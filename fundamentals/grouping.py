import httpx
import asyncio
from datetime import datetime, time

class Rasp:
    def __init__(self, rasp):
        self.__week_start = None
        self.__week_end = None
        self.__rasp = None
        grouped = self._group_by_date(rasp)
        if grouped:
            self._sort_pairs(grouped)
            self.__week_start = min(list(grouped.keys()))
            self.__week_end = max(list(grouped.keys()))
            self.__void_week = False
            self.__rasp = grouped
        else:
            self.__void_week = True


    def __str__(self):
        if self.__void_week:
            return "На этой неделе пар нет"
        out = ''
        for date, pairs in self.__rasp.items():
            out += f'{date}:\n\n'
            for pair in pairs:
                out += str(pair)
                out += '\n\n'
        return out

    @staticmethod
    def _group_by_date(rasp):
        grouped = dict()
        for pair in rasp:
            p = Pair(pair)
            date = str(p.date)
            if not date in grouped:
                grouped[date] = []
            grouped[date].append(p)
        return grouped

    @staticmethod
    def _sort_pairs(grouped_pairs):
        for pairs in grouped_pairs.values():
            pairs.sort(key=lambda pair: pair.start_time)

class Pair:
    def __init__(self, pair: dict):
        self.date = datetime.fromisoformat(pair['дата']).date()
        self.start_time = time.fromisoformat(pair['начало'])
        self.end_time = time.fromisoformat(pair['конец'])
        self.tutor = pair['преподаватель']
        self.cab = pair['аудитория']

    def __str__(self):
        return (f'Дата: {self.date}\nВремя начала: {self.start_time}\nВремя окончания: {self.end_time}\n'
                f'Преподаватель: {self.tutor}\nАудитория: {self.cab}')


async def get_rasp(url: str, date, group_id=73007):
    params = {
        "idGroup": group_id,
        "sdate": date
    }
    last_error = False
    retry_time = 2
    success = False
    async with httpx.AsyncClient(timeout=5) as client:
        for attempt in range(1, 4):
            if last_error:
                await asyncio.sleep(retry_time)

            last_error = False
            retry_time = 2
            print(f'Попытка {attempt}')
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                last_error = True
                response = e.response
                status = response.status_code
                match status:
                    case 429:
                        print("Ошибка. Слишком много запросов.")
                        try:
                            retime = response.headers.get("Retry-After")
                            if retime:
                                retry_time = int(retime)
                        except ValueError:
                            retry_time = 2

                    case 408:
                        print("Таймаут отправления запроса")
                        retry_time = 0

                    case 504:
                        print("Таймаут апстрим сервера")
                        retry_time = 10

                    case 404:
                        print("Ошибка. Ресурс не найден")
                        break
                    case 403:
                        print("Доступ запрещён")
                        break
                    case 502:
                        print("Ошибка запроса к вышестоящему серверу")
                    case 503:
                        print("Ошибка. Сервис временно недоступен")
                    case 500:
                        print("Внутренняя ошибка сервера.")
                    case _:
                        print("Ошибка при получении ответа от сервера.")
                        break
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
        data = response.json()
        return data['data']['rasp']



async def main():
    r = await get_rasp("https://edu.donstu.ru/api/Rasp", date="2026-11-16")
    rasp = Rasp(r)
    print(rasp)

if __name__ == "__main__":
    asyncio.run(main())
