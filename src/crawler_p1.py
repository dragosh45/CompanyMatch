#no async
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

def extract_company_data(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'lxml')

        # Extrage numere de telefon
        phones = set(re.findall(r'\+?\d[\d\s\-().]{7,}\d', soup.get_text()))

        # Extrage linkuri de social media
        links = [a['href'] for a in soup.find_all('a', href=True)]
        social_links = [link for link in links if any(s in link for s in [
            'facebook.com', 'linkedin.com', 'twitter.com', 'instagram.com'
        ])]

        return {
            "website": url,
            "phones": list(phones),
            "social_links": social_links
        }

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return {"website": url, "phones": [], "social_links": []}


def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    input_file = BASE_DIR / "data" / "sample-websites.csv"
    output_file = BASE_DIR / "data" / "scraped_data_no_async.csv"

    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return

    # Citește fără header, numește coloana "domain"
    df = pd.read_csv(input_file, header=None, names=["domain"])
    results = []

    for domain in df['domain']:
        url = f"https://{domain.strip()}"  # Adaugă protocolul
        data = extract_company_data(url)
        results.append(data)

    out_df = pd.DataFrame(results)
    out_df.to_csv(output_file, index=False)
    print(f" Scraping finished. Results saved to:\n{output_file}")



if __name__ == "__main__":
    main()
