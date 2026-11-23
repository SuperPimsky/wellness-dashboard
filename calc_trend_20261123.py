import json
from datetime import datetime, timedelta

raw = """2026-11-22T16:23:25.000Z 84.607
2026-11-20T11:59:34.000Z 83.553
2026-11-19T11:13:33.000Z 83.854
2026-11-18T11:17:46.000Z 83.649
2026-11-17T10:49:05.000Z 84.279
2026-11-16T11:37:44.000Z 84.210
2026-11-14T13:36:36.000Z 84.648
2026-11-13T12:25:02.000Z 84.593
2026-11-12T11:42:28.000Z 85.155
2026-11-11T11:40:44.000Z 84.799
2026-11-10T11:36:06.000Z 84.785
2026-11-09T11:37:26.000Z 85.059
2026-11-08T17:43:10.000Z 84.703
2026-11-07T12:57:28.000Z 85.853
2026-11-06T12:30:02.000Z 84.730
2026-11-05T12:01:53.000Z 84.854
2026-11-04T11:59:38.000Z 84.388
2026-11-03T15:44:45.000Z 83.882
2026-11-02T11:59:12.000Z 84.019
2026-11-01T13:09:11.000Z 83.745
2026-10-31T12:19:11.000Z 84.416
2026-10-30T12:47:10.000Z 84.785
2026-10-28T11:06:30.000Z 85.073
2026-10-27T10:34:34.000Z 85.593
2026-10-25T11:58:30.000Z 85.825
2026-10-24T12:12:54.000Z 86.332
2026-10-23T11:25:37.000Z 85.456
2026-10-22T11:00:43.000Z 86.031
2026-10-21T10:58:33.000Z 86.140
2026-10-20T10:57:01.000Z 86.387
2026-10-19T11:10:58.000Z 86.003
2026-10-18T16:33:06.000Z 86.715
2026-10-17T12:43:51.000Z 86.085
2026-10-15T11:03:28.000Z 86.154
2026-10-14T11:02:24.000Z 86.701
2026-10-13T10:53:08.000Z 86.373
2026-10-12T10:57:31.000Z 86.222
2026-10-11T17:25:41.000Z 85.798
2026-10-09T12:17:34.000Z 85.456
"""

entries = {}
for line in raw.strip().split("\n"):
    ts, w = line.split()
    d = ts.split("T")[0]
    w = float(w)
    if d not in entries:
        entries[d] = w
    else:
        entries[d] = (entries[d] + w) / 2

dates = sorted(entries.keys())

start = datetime.strptime("2026-10-09", "%Y-%m-%d")
end = datetime.strptime("2026-11-22", "%Y-%m-%d")
daily_kg = []
last_val = entries[dates[0]]
cur = start
while cur <= end:
    ds = cur.strftime("%Y-%m-%d")
    if ds in entries:
        last_val = entries[ds]
    daily_kg.append((ds, last_val))
    cur += timedelta(days=1)

ema = []
for i, (ds, val) in enumerate(daily_kg):
    if i == 0:
        ema.append(val)
    else:
        ema.append(ema[-1] + 0.1 * (val - ema[-1]))

def kg2lb(x):
    return x * 2.20462

trend_lb = [kg2lb(e) for e in ema]
dates_list = [x[0] for x in daily_kg]
today_idx = dates_list.index("2026-11-22")
idx_14 = today_idx - 14

trend_today = trend_lb[today_idx]
trend_14 = trend_lb[idx_14]
weekly_rate = (trend_today - trend_14) / 14 * 7

latest_actual_lb = kg2lb(entries["2026-11-22"])
prior_14d_date = dates_list[idx_14]
prior_actual_lb = kg2lb(entries.get(prior_14d_date, daily_kg[idx_14][1]))

goal_weight = 155
goal_date = datetime.strptime("2027-06-01", "%Y-%m-%d")
if weekly_rate < -0.05:
    weeks_needed = (trend_today - goal_weight) / (-weekly_rate)
    proj_date = datetime.strptime("2026-11-22", "%Y-%m-%d") + timedelta(weeks=weeks_needed)
    proj_str = proj_date.strftime("%Y-%m-%d")
    on_pace = proj_date <= goal_date
else:
    proj_str = "not on current pace"
    on_pace = False

out = {
    "trend_today_lb": round(trend_today, 2),
    "trend_14_lb": round(trend_14, 2),
    "weekly_rate_lb": round(weekly_rate, 3),
    "latest_actual_lb": round(latest_actual_lb, 1),
    "prior_actual_lb": round(prior_actual_lb, 1),
    "prior_date": prior_14d_date,
    "projected_goal_date": proj_str,
    "on_pace": on_pace,
}
print(json.dumps(out, indent=2))
