#second async with timeout 20 and 25 paralel requests

import asyncio
from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Funcția care extrage datele pentru un singur URL
async def fetch_data(session, url, semaphore):
    async with semaphore:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
            }
            async with session.get(url, timeout=20, headers=headers) as response:
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


# Funcția principală asincronă
async def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    input_file = BASE_DIR / "data" / "sample-websites.csv"
    output_file = BASE_DIR / "data" / "scraped_data_improved_only_https.csv"

    df = pd.read_csv(input_file, header=None, names=["domain"])
    urls = [f"https://{domain.strip()}" for domain in df["domain"]]

    semaphore = asyncio.Semaphore(25)  # mai puține requesturi în paralel pentru stabilitate

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

    pd.DataFrame(results).to_csv(output_file, index=False)
    print(f"Async scraping completed. Output saved to: {output_file}")


# Rulare
if __name__ == "__main__":
    import sys

    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f" Total time: {time.time() - start:.2f} seconds")
