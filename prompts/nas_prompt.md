# NAS Report Prompt

Fetch https://raw.githubusercontent.com/wisedonkey-sc/fitness-sync/main/latest_metrics.json and generate my NAS report using the data you find there.

---

CARDIAC CONTEXT:
- Bicuspid Aortic Valve + Ascending Aortic Aneurysm 4.7cm
- Meds: Metoprolol Succinate 50mg BD — blunts HR ~12 bpm
- All HR data must be adjusted +12 bpm before comparison to baselines
- Currently on Nervous System Stability Plan — Energy Bank target: 42-point baseline

NAS FORMULA:
- NAS = 0.65 * HRV_suppression + 0.35 * HR_elevation
- HR elevation: actual HR + 12 (Metoprolol offset) vs 14-day rolling median (p50)
- HRV suppression: deviation of SDNN below 14-day baseline
- Scale: 0-100. Low 0-25 | Medium 26-50 | High 51-100
- Dynamic threshold: if prior night sleep < 6.5h, drop all thresholds by 0.03

NAS TRIGGER THRESHOLDS:
- System Drain Flag: NAS >= 50 OR High Stress sedentary >= 60 min
- Cardiac Alert: High Stress sedentary > 90 min (excessive sympathetic load on aortic wall)
- NAS-4 Exhaustion Protocol: NAS >= 75 anytime | NAS >= 55 at 19:00 | Time in High >= 300 min | Energy Bank <= 15 after 15:00
- Sleep debt > 1h: subtract 8 from all thresholds

ZONE STATUS:
- Zone 1 (Buffer): Sleep Debt < 2h AND RR < 16.5 rpm
- Zone 2 (Strain): Sleep Debt 2-4h — walk only, no running
- Zone 3 (Cliff): Sleep Debt > 4h OR RR > 16.5 rpm — full rest recommended

SEDENTARY LIMITS:
- Max 40 min consecutive sedentary (30 min during 16:00-19:00)
- Daily ceiling: 420 min total sedentary

BASELINES:
- HRV SDNN: 50-60ms | RHR: high 40s-low 50s bpm | RR: ~14 rpm

---

Generate the NAS report in EXACTLY this format:

## 1. INTRA-DAY STRESS PROFILE

Narrative summary of stress accumulation across the day. Identify specific drain windows (e.g. 14:00-16:00 desk block). Reference hourly markers where data allows. Include time in each zone:
- Low stress (NAS 0-25): X min
- Medium stress (NAS 26-50): X min
- High stress (NAS 51-100): X min

## 2. SYSTEM DRAIN STATUS

- Current NAS estimate and zone
- System Drain Flag: TRIGGERED / CLEAR
- Cardiac Alert: TRIGGERED / CLEAR
- Zone status: Zone 1 (Buffer) / Zone 2 (Strain) / Zone 3 (Cliff)
- Energy Bank estimate vs 42-point target

## 3. METRIC CALIBRATION (DATA NERD LAYER)

- HRV SDNN: actual vs 50-60ms baseline (% deviation)
- RHR (Metoprolol-adjusted, +12 bpm): interpreted value vs median
- Resp Rate: actual vs 16.5 rpm threshold
- Sleep debt: estimated from prior night total vs 7.5h need
- Any dynamic threshold adjustments applied

## 4. DOWN-REGULATION PROTOCOL (if System Drain flagged)

If NAS >= 50 or Cardiac Alert triggered, prescribe one of:
- NSDR (10-20 min non-sleep deep rest)
- Physiological sigh (5 min: double inhale through nose, long exhale)
- 4-7-8 breathing (4 cycles minimum)
State which and why based on current NAS level and time of day.

CONSTRAINTS: No emojis. Strictly numeric and analytical. No motivational language. Data-anchored only.
