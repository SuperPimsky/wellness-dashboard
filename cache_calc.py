import datetime, json

raw = {
"2026-11-19":83.854,"2026-11-18":83.649,"2026-11-17":84.279,"2026-11-16":84.21,
"2026-11-14":84.648,"2026-11-13":84.593,"2026-11-12":85.155,"2026-11-11":84.799,
"2026-11-10":84.785,"2026-11-09":85.059,"2026-11-08":84.703,"2026-11-07":85.853,
"2026-11-06":84.73,"2026-11-05":84.854,"2026-11-04":84.388,"2026-11-03":83.882,
"2026-11-02":84.019,"2026-11-01":83.745,"2026-10-31":84.416,"2026-10-30":84.785,
"2026-10-28":85.073,"2026-10-27":85.593,"2026-10-25":85.825,"2026-10-24":86.332,
"2026-10-23":85.456,"2026-10-22":86.031,"2026-10-21":86.14,"2026-10-20":86.387,
"2026-10-19":86.003,"2026-10-18":86.715,"2026-10-17":86.085,"2026-10-15":86.154,
"2026-10-14":86.701,"2026-10-13":86.373,"2026-10-12":86.222,"2026-10-11":85.798,
"2026-10-09":85.456,"2026-10-05":86.455,
}

start = datetime.date(2026,10,5)
end = datetime.date(2026,11,19)
days = []
d = start
while d <= end:
    days.append(d)
    d += datetime.timedelta(days=1)

last_known = None
actual_lb = []
dates=[]
for d in days:
    key = d.isoformat()
    if key in raw:
        last_known = raw[key]*2.20462
    actual_lb.append(last_known)
    dates.append(key)

trend = [actual_lb[0]]
for i in range(1, len(actual_lb)):
    trend.append(trend[i-1] + 0.1*(actual_lb[i]-trend[i-1]))

out = {"dates": dates, "actual": [round(x,2) for x in actual_lb], "trend": [round(x,2) for x in trend]}

trend_today = trend[-1]
idx14 = len(dates)-1-14
trend_14 = trend[idx14]
weekly_rate = (trend_today - trend_14)/14*7

out["trend_today"] = round(trend_today,2)
out["trend_14"] = round(trend_14,2)
out["date14"] = dates[idx14]
out["weekly_rate_lb"] = round(weekly_rate,3)
out["latest_lb"] = round(83.854*2.20462,1)
out["prior_date_lb"] = round(raw["2026-11-05"]*2.20462,1)  # 14 days prior actual

print(json.dumps(out, indent=2))
