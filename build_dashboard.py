#!/usr/bin/env python3
"""
Builds index.html for the wellness daily dashboard (PeakWatch-style).
Run by a daily Hermes cron prompt that first pulls fresh data via MCP
(Oura oura_today, FoodNoms get_goal_progress, Hevy hevy_list_workouts,
Withings get_measures), fills in DATA below, then runs this script and
git commits/pushes.
"""
import json
import sys
from datetime import datetime

DATA = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}

def sparkline(values, lo=0, hi=100):
    bars = "▁▂▃▄▅▆▇█"
    out = []
    for v in values:
        if v is None:
            out.append(" ")
            continue
        idx = int((v - lo) / (hi - lo) * (len(bars) - 1))
        idx = max(0, min(len(bars) - 1, idx))
        out.append(bars[idx])
    return "".join(out)

def score_color(v):
    if v is None:
        return "#888"
    if v >= 85:
        return "#2ecc71"
    if v >= 70:
        return "#f1c40f"
    return "#e74c3c"

def pct(a, b):
    if not b:
        return 0
    return max(0, min(100, round(100 * a / b)))

d = DATA
readiness = d.get("readiness", {})
sleep = d.get("sleep", {})
nutrition = d.get("nutrition", {})
training = d.get("training", {})
weight = d.get("weight", {})
stress = d.get("stress")  # optional, may be None

today_label = d.get("date", datetime.now().strftime("%Y-%m-%d"))

r_score = readiness.get("score")
r_trend = readiness.get("trend", [])
r_contrib = readiness.get("contributors", {})

s_score = sleep.get("score")
s_trend = sleep.get("trend", [])
s_contrib = sleep.get("contributors", {})

cal_logged = nutrition.get("calories_logged", 0)
cal_target = nutrition.get("calories_target", 0)
protein_logged = nutrition.get("protein_logged", 0)
protein_target = nutrition.get("protein_target", 0)
water_logged = nutrition.get("water_logged", 0)
water_target = nutrition.get("water_target", 0)

last_workout = training.get("last_workout")
sessions_7d = training.get("sessions_7d", 0)

weight_latest = weight.get("latest")
weight_prior = weight.get("prior")
weight_unit = weight.get("unit", "lb")
weight_delta = None
if weight_latest is not None and weight_prior is not None:
    weight_delta = round(weight_latest - weight_prior, 1)

def contrib_row(label, val):
    return f"""<div class="crow"><span>{label}</span>
      <div class="cbar"><div class="cfill" style="width:{val or 0}%;background:{score_color(val)}"></div></div>
      <span class="cval">{val if val is not None else '—'}</span></div>"""

contrib_html_r = "\n".join(contrib_row(k.replace("_", " ").title(), v) for k, v in r_contrib.items())
contrib_html_s = "\n".join(contrib_row(k.replace("_", " ").title(), v) for k, v in s_contrib.items())

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Michael's Daily Wellness — {today_label}</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  body {{
    background: #0b0d10; color: #e8e8e8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    margin: 0; padding: 20px; max-width: 720px; margin-inline: auto;
  }}
  h1 {{ font-size: 1.4rem; margin-bottom: 2px; }}
  .sub {{ color: #888; font-size: 0.85rem; margin-bottom: 20px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }}
  .card {{
    background: #16191d; border-radius: 14px; padding: 16px; border: 1px solid #22262b;
  }}
  .card.full {{ grid-column: 1 / -1; }}
  .card h2 {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #9aa0a6; margin: 0 0 8px; }}
  .bigscore {{ font-size: 2.6rem; font-weight: 700; line-height: 1; }}
  .label {{ color: #9aa0a6; font-size: 0.8rem; margin-top: 2px; }}
  .spark {{ font-size: 1.3rem; letter-spacing: 1px; color: #5dade2; margin-top: 6px; }}
  .crow {{ display: flex; align-items: center; gap: 8px; font-size: 0.78rem; margin: 4px 0; }}
  .crow span:first-child {{ flex: 0 0 110px; color: #9aa0a6; }}
  .cbar {{ flex: 1; background: #22262b; border-radius: 4px; height: 6px; overflow: hidden; }}
  .cfill {{ height: 100%; border-radius: 4px; }}
  .cval {{ flex: 0 0 28px; text-align: right; }}
  .metricrow {{ display: flex; justify-content: space-between; font-size: 0.9rem; margin: 6px 0; }}
  .metricrow .v {{ font-weight: 600; }}
  .bar {{ background: #22262b; border-radius: 6px; height: 10px; overflow: hidden; margin-top: 4px; }}
  .barfill {{ height: 100%; border-radius: 6px; background: #5dade2; }}
  .note {{ color: #666; font-size: 0.75rem; margin-top: 8px; }}
  .pos {{ color: #2ecc71; }}
  .neg {{ color: #e74c3c; }}
  footer {{ text-align: center; color: #555; font-size: 0.7rem; margin-top: 30px; }}
</style>
</head>
<body>
<h1>Daily Wellness</h1>
<div class="sub">{today_label} · auto-generated</div>

<div class="grid">
  <div class="card">
    <h2>Recovery (Readiness)</h2>
    <div class="bigscore" style="color:{score_color(r_score)}">{r_score if r_score is not None else '—'}</div>
    <div class="label">out of 100</div>
    <div class="spark">{sparkline(r_trend)}</div>
    <div class="note">7-day trend, oldest → newest</div>
  </div>
  <div class="card">
    <h2>Sleep (last night)</h2>
    <div class="bigscore" style="color:{score_color(s_score)}">{s_score if s_score is not None else '—'}</div>
    <div class="label">out of 100</div>
    <div class="spark">{sparkline(s_trend)}</div>
    <div class="note">7-day trend, oldest → newest</div>
  </div>

  <div class="card full">
    <h2>Recovery Contributors</h2>
    {contrib_html_r}
  </div>

  <div class="card full">
    <h2>Sleep Contributors</h2>
    {contrib_html_s}
  </div>

  <div class="card">
    <h2>Energy & Stress</h2>
    <div class="metricrow"><span>Weight</span><span class="v">{weight_latest if weight_latest is not None else '—'} {weight_unit}</span></div>
    <div class="metricrow"><span>14-day change</span>
      <span class="v {'pos' if (weight_delta or 0) < 0 else ('neg' if (weight_delta or 0) > 0 else '')}">{('+' if (weight_delta or 0) > 0 else '') + str(weight_delta) + ' ' + weight_unit if weight_delta is not None else '—'}</span></div>
    <div class="note">{stress if stress else 'Stress score: not wired yet (Oura daily stress endpoint pending)'}</div>
  </div>

  <div class="card">
    <h2>Training Load</h2>
    <div class="metricrow"><span>Sessions, last 7d</span><span class="v">{sessions_7d}</span></div>
    <div class="metricrow"><span>Last workout</span><span class="v">{last_workout.get('date','—') if last_workout else '—'}</span></div>
    <div class="note">{last_workout.get('title','') if last_workout else ''}</div>
  </div>

  <div class="card full">
    <h2>Nutrition (today, in progress)</h2>
    <div class="metricrow"><span>Calories</span><span class="v">{cal_logged:.0f} / {cal_target:.0f} kcal</span></div>
    <div class="bar"><div class="barfill" style="width:{pct(cal_logged, cal_target)}%"></div></div>
    <div class="metricrow"><span>Protein</span><span class="v">{protein_logged:.0f} / {protein_target:.0f} g</span></div>
    <div class="bar"><div class="barfill" style="width:{pct(protein_logged, protein_target)}%;background:#9b59b6"></div></div>
    <div class="metricrow"><span>Water</span><span class="v">{water_logged:.0f} / {water_target:.0f} oz</span></div>
    <div class="bar"><div class="barfill" style="width:{pct(water_logged, water_target)}%;background:#5dade2"></div></div>
  </div>
</div>

<footer>Sources: Oura (recovery/sleep), Withings (weight), Hevy (training), FoodNoms (nutrition) · rebuilt daily via Hermes cron</footer>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)
print("wrote index.html")
