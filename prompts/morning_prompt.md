# Morning Report Prompt

Fetch https://raw.githubusercontent.com/wisedonkey-sc/fitness-sync/main/latest_metrics.json and generate my morning report using the data you find there.

---

CARDIAC CONTEXT (non-negotiable constraints):
- Bicuspid Aortic Valve + Mild Aortic Stenosis (PPG 20 mmHg)
- Ascending Aortic Aneurysm 4.7cm (surgical threshold 5.0-5.5cm)
- Mild Concentric LV Hypertrophy (LVPW-d 1.70cm May 2026, up from 1.40cm Dec 2025)
- EF 60% stable | Aortic root 3.70cm (up from 3.00cm Dec 2025)
- Meds: Metoprolol Succinate 50mg BD + Rosuvastatin 10mg alternate days
- Metoprolol blunts HR ~12 bpm — always adjust HR +12 for true stress analysis
- Hard limits: No HIIT, No Zone 4+, No heavy isometrics, No Valsalva, No back-to-back runs

BASELINES (30-day rolling):
- HRV rMSSD: 100-110ms (Oura overnight)
- HRV SDNN: 50-60ms (Apple Health)
- RHR: high 40s-low 50s bpm
- VO2max: 48 ml/kg/min (target 50+)
- SpO2: 97.2%
- Z2 operating target: 132-141 bpm (pace 6:15-6:35/km, NP 270-285W)
- EF target: 2.04 by end June 2026
- GCT target: <=260ms by end June 2026

GO/NO-GO THRESHOLDS:
- Run: Readiness >= 75 AND body_temp contributor >= 85
- Walk: Readiness 60-74
- Full rest: Readiness < 60
- HRV rMSSD >= 100ms to run | Rest if < 80ms
- RHR <= 54 bpm to run | Rest if > 62
- Body temp deviation <= +0.10C to run | Rest if > +0.35C
- NAS <= 25 (no workout if >= 51)
- Ambient temp <= 30C (trim 12% duration if > 30C)

---

Generate the morning report in EXACTLY this format:

## 1. THE DAILY FOUR-METRIC DASHBOARD

| Metric | Value | Status |
|---|---|---|
| Sleep Score (Oura) | | |
| Readiness (Oura) | | |
| HRV rMSSD (Oura) | | vs 100-110ms baseline |
| HRV SDNN (Apple Health) | | vs 50-60ms baseline |

## 2. PERFORMANCE ANALYSIS

- Compare every metric against baseline (express as % above/below, e.g. "HRV rMSSD 12% below baseline")
- Apply +12 bpm Metoprolol correction to all HR values before stress interpretation
- Sleep architecture breakdown: Total / Deep / REM / Light hours
- SpO2, Resp Rate, Wrist Temp flags if outside normal
- Today's recommended activity: specific session type, duration, HR zone, pace

## 3. THE SO WHAT

- Causation/correlations (e.g. "Late dinner -> elevated RHR -> compressed deep sleep")
- One specific experiment to run today or tonight
- Cardiac guardrails: flag any metric > 1.5 SD from baseline

CONSTRAINTS: No emojis. No corporate pleasantries. Direct, factual, data-anchored only.
