import pandas as pd

def analyze_data(file_path):
    df = pd.read_csv(file_path)
    total = len(df)
    with_phones = df['phones'].apply(lambda x: len(eval(x)) > 0).sum()
    with_social = df['social_links'].apply(lambda x: len(eval(x)) > 0).sum()

    print(f"Total websites crawled: {total}")
    print(f"Websites with phone numbers: {with_phones} ({with_phones / total:.2%})")
    print(f"Websites with social media links: {with_social} ({with_social / total:.2%})")

if __name__ == "__main__":
    print("---->Data analyze for data without using async")
    analyze_data(r"C:/Users/drago/OneDrive/Documents/prepare interviews/fromRealInterview_and_preparation/veridion/company_scraper_project/data/scraped_data_no_async.csv")
    print("---->Data analyze for data using async")
    analyze_data(r"C:/Users/drago/OneDrive/Documents/prepare interviews/fromRealInterview_and_preparation/veridion/company_scraper_project/data/scraped_data_async.csv")
    print("----->Data analyze for data using async fallback to http with modified")
    analyze_data(r"C:/Users/drago/OneDrive/Documents/prepare interviews/fromRealInterview_and_preparation/veridion/company_scraper_project/data/scraped_data_async_improved.csv")
