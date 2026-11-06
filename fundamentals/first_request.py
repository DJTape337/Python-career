import json
import httpx
from datetime import datetime, timedelta
for attempt in range(1, 4):
    try:
        response = httpx.get('https://edu.donstu.ru/api/Rasp?idGroup=73007&sdate=2026-10-20',
                             timeout=5)
        response.raise_for_status()
    except httpx.TimeoutException:
        print("Сервер не ответил вовремя")
        raise SystemExit(1)
    except httpx.RequestError:
        print("Не удалось выполнить запрос.")
        raise SystemExit(1)
    except httpx.HTTPStatusError:
        print("Сервер вернул ошибочный статус")
        raise SystemExit(1)
    else:
        break
j = response.json()
with open('response.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(j, indent=4, ensure_ascii=False))

rasp = j['data']['rasp']
pair1 = rasp[0]
pair2 = rasp[1]
time1 = datetime.fromisoformat(pair1['датаОкончания'])
time2 = datetime.fromisoformat(pair2['датаНачала'])
brtime = time2 - time1
if brtime >= timedelta(minutes=45):
    print("Перерыв подходит")
else:
    print("Перерыв не подходит")


