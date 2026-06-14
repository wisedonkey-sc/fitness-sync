#!/usr/bin/env python3
"""
fetch_latest.py — Sudeep's Fitness Data Fetcher (Oura + Apple Health)
======================================================================
Sources:
  - Oura API (readiness, sleep, HRV rMSSD)
  - Apple Health CSV exported by Health Auto Export app

Output: latest_metrics.json in the same directory as this script.

Credentials: reads from environment variables (set as GitHub Actions secrets):
  OURA_TOKEN            — Oura personal access token
  APPLE_HEALTH_CSV_DIR  — path to folder containing HealthMetrics-YYYY-MM-DD.csv files
                          (not needed in GitHub Actions — Health Auto Export uploads directly)
"""

import json
import os
import sys
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path

HERE        = Path(__file__).parent
OUTPUT_PATH = HERE / "latest_metrics.json"

TODAY     = date.today()
YESTERDAY = TODAY - timedelta(days=1)


# ── Dependency installer ──────────────────────────────────────────────────────
def ensure_deps():
    for pkg in ["requests"]:
        try:
            __import__(pkg)
        except ImportError:
            print(f"Installing {pkg}...")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg,
                            "--quiet", "--break-system-packages"], check=True)


# ── Oura ──────────────────────────────────────────────────────────────────────
def fetch_oura(token: str) -> dict:
    import requests
    headers = {"Authorization": f"Bearer {token}"}
    base    = "https://api.ouraring.com/v2/usercollection"

    def get(endpoint, params):
        r = requests.get(f"{base}/{endpoint}", headers=headers, params=params, timeout=15)
        r.raise_for_status()
        return {rec["day"]: rec for rec in r.json().get("data", [])}

    params = {"start_date": YESTERDAY.isoformat(), "end_date": TODAY.isoformat()}

    readiness   = get("daily_readiness", params)
    daily_sleep = get("daily_sleep",     params)
    activity    = get("daily_activity",  params)
    spo2        = get("daily_spo2",      params)

    # Raw sleep sessions for rMSSD + stage hours
    sleep_raw = requests.get(f"{base}/sleep", headers=headers, params=params, timeout=15)
    sleep_raw.raise_for_status()
    sleep_by_day: dict[str, dict] = {}
    for s in sleep_raw.json().get("data", []):
        day = s.get("day", "")
        if day not in sleep_by_day:
            sleep_by_day[day] = {"total_s": 0, "deep_s": 0, "rem_s": 0, "light_s": 0,
                                  "hrv_vals": [], "hr_vals": [], "eff_vals": []}
        acc = sleep_by_day[day]
        acc["total_s"] += s.get("total_sleep_duration", 0) or 0
        acc["deep_s"]  += s.get("deep_sleep_duration",  0) or 0
        acc["rem_s"]   += s.get("rem_sleep_duration",   0) or 0
        acc["light_s"] += s.get("light_sleep_duration", 0) or 0
        if s.get("average_hrv"):       acc["hrv_vals"].append(s["average_hrv"])
        if s.get("lowest_heart_rate"): acc["hr_vals"].append(s["lowest_heart_rate"])
        if s.get("efficiency"):        acc["eff_vals"].append(s["efficiency"])

    def hr_to(sec): return round(sec / 3600, 2) if sec else None
    def mean(lst):  return round(sum(lst) / len(lst), 1) if lst else None

    sleep_sessions = {}
    for day, acc in sleep_by_day.items():
        sleep_sessions[day] = {
            "total_hr":  hr_to(acc["total_s"]),
            "deep_hr":   hr_to(acc["deep_s"]),
            "rem_hr":    hr_to(acc["rem_s"]),
            "light_hr":  hr_to(acc["light_s"]),
            "hrv_rmssd": mean(acc["hrv_vals"]),
            "lowest_hr": min(acc["hr_vals"]) if acc["hr_vals"] else None,
            "efficiency":mean(acc["eff_vals"]),
        }

    def day_data(d):
        ds = d.isoformat()
        r  = readiness.get(ds, {})
        sl = daily_sleep.get(ds, {})
        ac = activity.get(ds, {})
        sp = spo2.get(ds, {})
        ss = sleep_sessions.get(ds, {})
        return {
            "readiness_score":       r.get("score"),
            "readiness_hrv_balance": r.get("contributors", {}).get("hrv_balance"),
            "readiness_temp_contrib":r.get("contributors", {}).get("body_temperature"),
            "sleep_score":           sl.get("score"),
            "sleep_total_hr":        ss.get("total_hr"),
            "sleep_deep_hr":         ss.get("deep_hr"),
            "sleep_rem_hr":          ss.get("rem_hr"),
            "sleep_light_hr":        ss.get("light_hr"),
            "sleep_hrv_rmssd":       ss.get("hrv_rmssd"),
            "sleep_lowest_hr":       ss.get("lowest_hr"),
            "sleep_efficiency":      ss.get("efficiency"),
            "steps":                 ac.get("steps"),
            "active_calories":       ac.get("active_calories"),
            "spo2_avg":              sp.get("spo2", {}).get("average") if sp else None,
        }

    return {"today": day_data(TODAY), "yesterday": day_data(YESTERDAY)}


# ── Apple Health (CSV from Health Auto Export) ────────────────────────────────
def fetch_apple_health(export_path: str) -> dict:
    import csv

    def read_day(d: date) -> dict:
        path = Path(export_path) / f"HealthMetrics-{d.isoformat()}.csv"
        if not path.exists():
            print(f"  Apple Health: no file for {d} at {path}")
            return {}

        metrics = {
            "steps":         "Step Count",
            "rhr":           "Resting Heart Rate",
            "hrv_sdnn":      "Heart Rate Variability",
            "spo2":          "Blood Oxygen Saturation",
            "resp_rate":     "Respiratory Rate",
            "active_energy": "Active Energy",
            "vo2max":        "VO2 Max",
            "weight_lb":     "Weight",
            "body_fat_pct":  "Body Fat Percentage",
            "wrist_temp":    "Apple Sleeping Wrist Temperature",
            # Garmin-synced workout fields (present if Garmin→AH sync is on)
            "workout_avg_hr":   "Workout Average Heart Rate",
            "workout_max_hr":   "Workout Max Heart Rate",
            "workout_dist_km":  "Workout Distance",
            "workout_duration": "Workout Duration",
            "workout_calories": "Workout Active Energy",
        }

        sums  = {"steps": 0, "active_energy": 0, "workout_dist_km": 0,
                  "workout_duration": 0, "workout_calories": 0}
        means = {k: [] for k in ["rhr", "hrv_sdnn", "spo2", "resp_rate",
                                  "vo2max", "workout_avg_hr", "workout_max_hr"]}
        lasts = {k: None for k in ["weight_lb", "body_fat_pct", "wrist_temp"]}

        try:
            with open(path, encoding="utf-8", newline="") as f:
                reader  = csv.reader(f)
                headers = next(reader)
                col = {}
                for key, substr in metrics.items():
                    for i, h in enumerate(headers):
                        if substr.lower() in h.lower():
                            col[key] = i
                            break
                for row in reader:
                    for key, idx in col.items():
                        if idx >= len(row): continue
                        try:    v = float(row[idx])
                        except: continue
                        if key in sums:   sums[key]  += v
                        elif key in means: means[key].append(v)
                        elif key in lasts: lasts[key] = v
        except Exception as e:
            print(f"  Apple Health warning ({d}): {e}")
            return {}

        result = {}
        for k, v in sums.items():
            result[k] = round(v, 1) if v else None
        for k, vals in means.items():
            result[k] = round(sum(vals) / len(vals), 1) if vals else None
        result.update(lasts)
        return result

    return {"today": read_day(TODAY), "yesterday": read_day(YESTERDAY)}


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    ensure_deps()

    oura_token        = os.environ.get("OURA_TOKEN", "")
    apple_health_path = os.environ.get("APPLE_HEALTH_CSV_DIR", "")

    print(f"Fetching fitness data for {TODAY.isoformat()}...")
    output = {
        "generated_at": datetime.now().isoformat(),
        "date":         TODAY.isoformat(),
        "oura":         {},
        "apple_health": {},
        "errors":       [],
    }

    # Oura
    if oura_token:
        try:
            print("Oura: fetching...")
            output["oura"] = fetch_oura(oura_token)
            print("Oura: done")
        except Exception as e:
            msg = f"Oura error: {e}"
            print(msg)
            output["errors"].append(msg)
    else:
        output["errors"].append("Oura: no token configured (set OURA_TOKEN secret)")

    # Apple Health
    if apple_health_path:
        try:
            print("Apple Health: reading CSVs...")
            output["apple_health"] = fetch_apple_health(apple_health_path)
            print("Apple Health: done")
        except Exception as e:
            msg = f"Apple Health error: {e}"
            print(msg)
            output["errors"].append(msg)
    else:
        print("Apple Health: APPLE_HEALTH_CSV_DIR not set — skipping (expected in GitHub Actions)")

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nWritten to: {OUTPUT_PATH}")

    # Summary
    o = output["oura"].get("today", {})
    a = output["apple_health"].get("today", {})

    print("\n── Today's snapshot ──────────────────────")
    print(f"Readiness:    {o.get('readiness_score', '—')}/100")
    print(f"Sleep:        {o.get('sleep_total_hr', '—')}h  "
          f"(Deep {o.get('sleep_deep_hr','—')}h  REM {o.get('sleep_rem_hr','—')}h)")
    print(f"HRV rMSSD:    {o.get('sleep_hrv_rmssd','—')} ms")
    print(f"HRV SDNN:     {a.get('hrv_sdnn','—')} ms")
    print(f"RHR:          {a.get('rhr','—')} bpm")
    print(f"Steps:        {o.get('steps') or a.get('steps','—')}")
    print(f"SpO2:         {o.get('spo2_avg') or a.get('spo2','—')}%")
    print(f"Resp Rate:    {a.get('resp_rate','—')} rpm")

    if output["errors"]:
        print(f"\nWarnings: {'; '.join(output['errors'])}")


if __name__ == "__main__":
    main()

