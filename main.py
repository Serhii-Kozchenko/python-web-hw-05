

import aiohttp
import asyncio
import platform
import sys
from datetime import datetime, timedelta


class HttpError(Exception):
    pass


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HttpError(f"Error status: {resp.status} for {url}")
        except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
            raise HttpError(f'Connection error: {url}', str(err))


async def main(period):
    try:
        result = []
        if period > 10:
            period = 10
            print("The exchange rate is provided for the last 10 days")
        

        for i in range(period):
            today = datetime.now()
            d = today - timedelta(days=i)
            shift = d.strftime("%d.%m.%Y")
            response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={shift}')
            if response:
                currency_course = {shift: {rate['currency']: {'sale': rate['saleRateNB'], 'purchase': rate['purchaseRateNB']}
                                           for rate in response['exchangeRate'] if rate['currency'] in ['USD', 'EUR']}}
                result.append(currency_course)
        return result
    except HttpError as err:
        print(err)
        return None

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    period = int(sys.argv[1])
    r = asyncio.run(main(period))
    print(r)
