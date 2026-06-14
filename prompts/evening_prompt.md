# Evening Report Prompt

Fetch https://raw.githubusercontent.com/wisedonkey-sc/fitness-sync/main/latest_metrics.json and generate my evening report using the data you find there.

---

CARDIAC CONTEXT (non-negotiable constraints):
- Bicuspid Aortic Valve + Mild Aortic Stenosis (PPG 20 mmHg)
- Ascending Aortic Aneurysm 4.7cm (surgical threshold 5.0-5.5cm)
- Mild Concentric LV Hypertrophy (LVPW-d 1.70cm May 2026)
- Meds: Metoprolol Succinate 50mg BD — blunts HR ~12 bpm, adjust +12 for stress analysis
- Hard limits: No HIIT, No Zone 4+, No heavy isometrics, No back-to-back runs

BASELINES:
- HRV rMSSD: 100-110ms | HRV SDNN: 50-60ms | RHR: high 40s-low 50s bpm
- Weekly structure: Sunday long run (500-650 kcal), Tuesday moderate, Friday stout
- Step floor: 7,400/day
- Target bedtime: 9:15-10:15 PM | Digital sunset: 22:00 absolute
- Sleep target: >= 80 Oura score
- Last meal: 3:00-4:00 PM | Zero caffeine | Minimal/zero alcohol (-10 readiness points)

NAS THRESHOLDS (Non-Activity Stress, scale 0-100):
- System Drain Flag: NAS >= 50 OR High Stress sedentary >= 60 min
- Cardiac Alert: High Stress sedentary > 90 min
- Sleep debt > 1h: subtract 8 from all NAS thresholds
- Checkpoints: Noon 28 | 15:00 40 | 18:00 50 | 19:00 54
- Sedentary max: 40 min consecutive (30 min during 16:00-19:00)
- Energy Bank target: 42-point baseline

SLEEP DEBT ZONES:
- Low: > 0h | Moderate: >= 2h | High: >= 5h
- Zone 1 (Buffer): Sleep Debt < 2h
- Zone 2 (Strain): Sleep Debt 2-4h — walk only, no running
- Zone 3 (Cliff): Sleep Debt > 4h or RR > 16.5 rpm — full rest

---

Generate the evening report in EXACTLY this format:

## 1. MINI RECAP

- Today's activity: type, duration, HR, distance
- Strain score (0-21 scale)
- Steps: actual vs 7,400 floor (surplus or deficit)

## 2. WEEKLY FIT & TOMORROW'S IMPLICATION

- How today fits the Sunday/Tuesday/Friday framework
- Tomorrow's prescribed session: type, duration, target HR zone, pace

## 3. STRESS & NAS ANALYSIS

- Inactive stress vs baseline (all HR adjusted +12 bpm for Metoprolol)
- Estimated NAS status and zone (Low/Medium/High)
- System Drain Flag or Cardiac Alert if triggered
- Weekly stress trend: climbing, stable, or recovering

## 4. SLEEP TIMING

- Estimated sleep debt (based on tonight's Oura sleep total vs 7.5h need)
- Target bedtime and wake time for tomorrow
- Consistency check vs 9:15-10:15 PM window

## 5. THE SO WHAT

- Specific down-regulation protocol if NAS elevated (NSDR, physiological sigh, etc.)
- One closing question about tomorrow's plan

CONSTRAINTS: No emojis. Data-anchored. Concise. No corporate pleasantries.
