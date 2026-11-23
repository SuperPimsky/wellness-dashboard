import json
from datetime import date, timedelta

raw = [
{"date":"2026-11-23","weight_kg":85.73},
{"date":"2026-11-22","weight_kg":84.607},
{"date":"2026-11-20","weight_kg":83.553},
{"date":"2026-11-19","weight_kg":83.854},
{"date":"2026-11-18","weight_kg":83.649},
{"date":"2026-11-17","weight_kg":84.279},
{"date":"2026-11-16","weight_kg":84.21},
{"date":"2026-11-14","weight_kg":84.648},
{"date":"2026-11-13","weight_kg":84.593},
{"date":"2026-11-12","weight_kg":85.155},
{"date":"2026-11-11","weight_kg":84.799},
{"date":"2026-11-10","weight_kg":84.785},
{"date":"2026-11-09","weight_kg":85.059},
{"date":"2026-11-08","weight_kg":84.833},
{"date":"2026-11-07","weight_kg":85.853},
{"date":"2026-11-06","weight_kg":84.73},
{"date":"2026-11-05","weight_kg":84.854},
{"date":"2026-11-04","weight_kg":84.388},
{"date":"2026-11-03","weight_kg":83.882},
{"date":"2026-11-02","weight_kg":84.019},
{"date":"2026-11-01","weight_kg":83.745},
{"date":"2026-10-31","weight_kg":84.416},
{"date":"2026-10-30","weight_kg":84.785},
{"date":"2026-10-28","weight_kg":85.073},
{"date":"2026-10-27","weight_kg":85.593},
{"date":"2026-10-25","weight_kg":85.825},
{"date":"2026-10-24","weight_kg":86.332},
{"date":"2026-10-23","weight_kg":85.456},
{"date":"2026-10-22","weight_kg":86.031},
{"date":"2026-10-21","weight_kg":86.14},
{"date":"2026-10-20","weight_kg":86.387},
{"date":"2026-10-19","weight_kg":86.003},
{"date":"2026-10-18","weight_kg":86.715},
{"date":"2026-10-17","weight_kg":86.085},
{"date":"2026-10-15","weight_kg":86.154},
{"date":"2026-10-14","weight_kg":86.701},
{"date":"2026-10-13","weight_kg":86.373},
{"date":"2026-10-12","weight_kg":86.222},
{"date":"2026-10-11","weight_kg":85.798},
{"date":"2026-10-09","weight_kg":85.456},
]

day_weight = {r["date"]: r["weight_kg"] for r in raw}

start = date(2026,10,9)
end = date(2026,11,23)
days = []
cur = start
while cur <= end:
    days.append(cur.isoformat())
    cur += timedelta(days=1)

actual = []
last = None
for d in days:
    kg = day_weight.get(d)
    if kg is not None:
        last = kg
    actual.append(last)

first_idx = next(i for i,v in enumerate(actual) if v is not None)
for i in range(first_idx):
    actual[i] = actual[first_idx]

lb = [a*2.20462 for a in actual]

trend = [lb[0]]
for i in range(1, len(lb)):
    trend.append(trend[-1] + 0.1*(lb[i]-trend[-1]))

trend_today = trend[-1]
trend_14ago = trend[-15]
weekly_rate = (trend_today - trend_14ago)/14*7

print("today", days[-1], "trend_today", round(trend_today,2))
print("14ago", days[-15], "trend_14ago", round(trend_14ago,2))
print("weekly_rate_lb", round(weekly_rate,3))
print("latest actual lb", round(lb[-1],1), "14d-ago actual lb", round(lb[-15],1))

goal=155
if weekly_rate < -0.05:
    weeks_needed = (trend_today - goal)/(-weekly_rate)
    proj_date = date(2026,11,23) + timedelta(weeks=weeks_needed)
    on_pace = proj_date <= date(2027,6,1)
    print("projected_goal_date", proj_date.isoformat(), "on_pace", on_pace)
else:
    print("not on current pace")

# print last 8 trend values for readiness/sleep spark reference not needed here
print("trend_weight_rounded", round(trend_today,1))
