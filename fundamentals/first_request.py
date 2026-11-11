import json
import time
import httpx
from datetime import datetime, timedelta


last_error = False
retry_time = 2
success = False
for attempt in range(1, 4):
    if last_error:
        time.sleep(retry_time)

    last_error = False
    retry_time = 2
    print(f'Попытка {attempt}')
    try:
        response = httpx.get('https://edu.donstu.ru/api/Rasp?idGroup=73007&sdate=2026-10-20',
                             timeout=5)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        last_error = True
        response = e.response
        status = response.status_code
        match status:
            case 429:
                retime = int(response.headers.get("Retry-After"))
                if retime:
                    retry_time = retime
                print("Ошибка. Слишком много запросов.")
            case 404:
                print("Ошибка. Ресурс не найден")
                break
            case 403:
                print("Доступ запрещён")
                break
            case 502:
                print("Ошибка запроса к вышестоящему серверу")
                break
            case 503:
                print("Ошибка. Сервис временно недоступен")
            case 500:
                print("Внутренняя ошибка сервера.")
    except httpx.TimeoutException:
        print("Превышено ожидание ответа сервера")
        last_error = True
    except httpx.RequestError:
        print("Ошибка запроса")
        last_error = True

    else:
        success = True
        break
if not success:
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


