import json, datetime

raw = [
("2026-11-20",83.553),("2026-11-19",83.854),("2026-11-18",83.649),("2026-11-17",84.279),
("2026-11-16",84.210),("2026-11-14",84.648),("2026-11-13",84.593),("2026-11-12",85.155),
("2026-11-11",84.799),("2026-11-10",84.785),("2026-11-09",85.059),
("2026-11-08",84.703),("2026-11-08",84.963),
("2026-11-07",85.853),("2026-11-06",84.730),("2026-11-05",84.854),("2026-11-04",84.388),
("2026-11-03",83.882),("2026-11-02",84.019),("2026-11-01",83.745),("2026-10-31",84.416),
("2026-10-30",84.785),("2026-10-28",85.073),("2026-10-27",85.593),("2026-10-25",85.825),
("2026-10-24",86.332),("2026-10-23",85.456),("2026-10-22",86.031),("2026-10-21",86.140),
("2026-10-20",86.387),("2026-10-19",86.003),("2026-10-18",86.715),("2026-10-17",86.085),
("2026-10-15",86.154),("2026-10-14",86.701),("2026-10-13",86.373),("2026-10-12",86.222),
("2026-10-11",85.798),("2026-10-09",85.456),("2026-10-05",86.455),("2026-10-04",86.414),
]

by_day = {}
for d,v in raw:
    by_day.setdefault(d, []).append(v)
by_day = {d: sum(v)/len(v) for d,v in by_day.items()}

start = datetime.date(2026,10,4)
end = datetime.date(2026,11,20)
days = []
d = start
while d <= end:
    days.append(d.isoformat())
    d += datetime.timedelta(days=1)

actual = []
last = None
for day in days:
    if day in by_day:
        last = by_day[day]
    actual.append(last)

first_idx = next(i for i,v in enumerate(actual) if v is not None)
trend = [None]*len(actual)
trend[first_idx] = actual[first_idx]
for i in range(first_idx+1, len(actual)):
    a = actual[i] if actual[i] is not None else trend[i-1]
    trend[i] = trend[i-1] + 0.1*(a - trend[i-1])

for day, a, t in zip(days, actual, trend):
    print(day, a, round(t,3) if t else t)

idx_today = days.index("2026-11-20")
idx_14ago = days.index("2026-11-06")
trend_today_kg = trend[idx_today]
trend_14ago_kg = trend[idx_14ago]
lb = 2.20462
trend_today_lb = trend_today_kg*lb
trend_14ago_lb = trend_14ago_kg*lb
weekly_rate = (trend_today_lb - trend_14ago_lb)/14*7
print("trend_today_lb", round(trend_today_lb,2))
print("trend_14ago_lb", round(trend_14ago_lb,2))
print("weekly_rate_lb", round(weekly_rate,3))

latest_lb = 83.553*lb
print("latest_lb", round(latest_lb,2))
