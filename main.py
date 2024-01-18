import pytz
import lxml
import time
import aiohttp
import asyncio
from sqlite3 import connect
from datetime import datetime
from bs4 import BeautifulSoup as BS
from module.module import Auth

auth = Auth(token='908b6f1a-4d34-4dee-8025-b385e9a82ec2').tokenCheck()

count = 1
async def getPage(proxy: str = None) -> int:
	async with aiohttp.ClientSession() as session:
		async with session.get('https://arzon.tj/catalog', proxy=proxy) as response:
			status_code = response.status
			text = await response.text()
			soup = BS(text, 'lxml')
			page = int(soup.find_all('a', class_="pagination__link link")[-1].text.strip())
			return page

async def dataCollection(page: int, proxy: str = None) -> None:
	global count
	try:
		async with aiohttp.ClientSession() as session:
			async with session.get(f'https://arzon.tj/catalog/page/{page}', proxy=proxy) as response:
				status_code = response.status
				text = await response.text()
				soup = BS(text, 'lxml')
				data = soup.find_all('div', class_='items-element__body items-element__body--pad')
				for i in data:
					title = i.find('a', class_="items-element__title").text.strip()
					link = i.find('a', class_="items-element__title").get('href')
					price = i.find('div', class_="item-info__price").text.strip()
					location = i.find('div', class_="item-info__address _hide-mob").find('span').text.strip()
					date = i.find('div', class_="item-info__date").find('span').text.strip()
					print(count, date, location, title, link, f'<{page}>')
					count += 1
	except Exception as error:
		print(f'[!] {error}')

async def main() -> None:
	task = []
	for i in range(1, await getPage()):
		task.append(asyncio.create_task(dataCollection(i)))

	await asyncio.gather(*task)

asyncio.run(main())