from datetime import datetime, time

date = datetime.fromisoformat("2026-11-23").date()

first_end = time(10, 0)
second_start = time(11, 30)

first_end = datetime.combine(date, first_end)
second_start = datetime.combine(date, second_start)

brtime = (second_start - first_end).total_seconds() / 60
print(brtime)
