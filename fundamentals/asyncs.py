import asyncio
import httpx

async def get_schedule(client, date, idGroup=73007):
	url = "https://edu.donstu.ru/api/Rasp" + date
	params = {
		"idGroup": idGroup,
		"sdate": date
	}
	response = await client.get(url, params=params)
	j = response.json
	l = len(j['data']['rasp'])
	print(f"Количество занятий {date}: {l}")
	return l
	
async def main():
	with httpx.AsyncClient(timeout=5) as client:
		lens = await asyncio.gather(
			get_schedule(client, "2026-11-1"),
			get_schedule(client, "2026-11-2"),
			get_schedule(client, "2026-11-3")
		)
	
if __name__ == "__main__":
	asyncio.run(main())
