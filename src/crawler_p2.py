#first async with timeout 10 and 50 paralel requests


from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import re

async def fetch_data(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=10) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'lxml')

                phones = set(re.findall(r'\+?\d[\d\s\-().]{7,}\d', soup.get_text()))
                links = [a['href'] for a in soup.find_all('a', href=True)]
                social_links = [
                    link for link in links if any(s in link for s in [
                        'facebook.com', 'linkedin.com', 'twitter.com', 'instagram.com'
                    ])
                ]

                return {
                    "website": url,
                    "phones": list(phones),
                    "social_links": social_links
                }

        except Exception as e:
            print(f"Error on {url}: {e}")
            return {"website": url, "phones": [], "social_links": []}


async def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    input_file = BASE_DIR / "data" / "sample-websites.csv"
    output_file = BASE_DIR / "data" / "scraped_data_async.csv"

    df = pd.read_csv(input_file, header=None, names=["domain"])
    urls = [f"https://{domain.strip()}" for domain in df["domain"]]

    semaphore = asyncio.Semaphore(50)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

    pd.DataFrame(results).to_csv(output_file, index=False)
    print(f"Async scraping completed. Output saved to: {output_file}")


if __name__ == "__main__":
    import sys
    import asyncio
    import time

    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f"⏱ Total time: {time.time() - start:.2f} seconds")

