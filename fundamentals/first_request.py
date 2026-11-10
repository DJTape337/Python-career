import json
import time
import httpx
from datetime import datetime, timedelta
for attempt in range(1, 4):
    print(f'Попытка {attempt}')
    try:
        response = httpx.get('https://edu.donstu.ru/api/Rasp?idGroup=73007&sdate=2026-10-20',
                             timeout=5)
        response.raise_for_status()
    except httpx.TimeoutException:
        print("Сервер не ответил вовремя")
        time.sleep(2)
    except httpx.RequestError:
        print("Не удалось выполнить запрос.")
        time.sleep(2)
    except httpx.HTTPStatusError:
        print("Сервер вернул ошибочный статус")
        time.sleep(2)
    else:
        break
else:
    print("Все попытки неудачны")
    raise SystemExit(1)
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


