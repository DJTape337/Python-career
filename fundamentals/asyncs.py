import asyncio
import json
import httpx

async def get_schedule(client, date, id_group=73007):
	url = "https://edu.donstu.ru/api/Rasp"
	params = {
		"idGroup": id_group,
		"sdate": date
	}
	response = await client.get(url, params=params)
	response.raise_for_status()
	j = response.json()
	l = len(j['data']['rasp'])
	print(f"Количество занятий {date}: {l}")
	return j
	
async def main():
	async with httpx.AsyncClient(timeout=5) as client:
		pairs = await asyncio.gather(
			get_schedule(client, "2026-11-01"),
			get_schedule(client, "2026-11-02"),
			get_schedule(client, "2026-11-03")
		)
		print(json.dumps(pairs, indent=4))
	
if __name__ == "__main__":
	asyncio.run(main())
