import datetime
trend_today = 186.284  # approx from earlier calc (84.495*2.20462)
trend_today = 84.495*2.20462
goal = 155.0
rate = -0.582  # lb/wk
weeks_needed = (trend_today - goal) / abs(rate)
days_needed = weeks_needed * 7
proj_date = datetime.date(2026,11,20) + datetime.timedelta(days=round(days_needed))
print("trend_today_lb", round(trend_today,2))
print("weeks_needed", round(weeks_needed,1))
print("projected_goal_date", proj_date.isoformat())
goal_date = datetime.date(2027,6,1)
print("on_pace", proj_date <= goal_date)
