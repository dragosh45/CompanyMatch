from pathlib import Path

import pandas as pd
import ast

def extract_facebook(social_links_str):
    try:
        links = ast.literal_eval(social_links_str)
        for link in links:
            if "facebook.com" in link:
                return link
    except:
        pass
    return ""

def merge_for_api_input(scraped_path, names_path, output_path):
    # Load input data
    scraped_df = pd.read_csv(scraped_path, dtype=str).fillna("")
    names_df = pd.read_csv(names_path, dtype=str).fillna("")

    # Normalize domain
    scraped_df["domain"] = scraped_df["website"].str.replace("https://", "").str.replace("http://", "").str.strip("/")
    names_df["domain"] = names_df["domain"].str.replace("https://", "").str.replace("http://", "").str.strip("/")

    # Merge on domain
    merged_df = pd.merge(scraped_df, names_df, on="domain", how="left")

    # Extract final columns
    merged_df["input name"] = merged_df["company_commercial_name"]
    merged_df["input website"] = merged_df["website"]
    merged_df["input phone"] = merged_df["phones"]
    merged_df["input_facebook"] = merged_df["social_links"].apply(extract_facebook)

    # Select only required columns
    final_df = merged_df[["input name", "input phone", "input website", "input_facebook"]]

    # Save to output
    final_df.to_csv(output_path, index=False)
    print(f"----> Merged data saved to: {output_path}")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    names_path = BASE_DIR / "data" / "sample-websites-company-names.csv"
    scraped_path = BASE_DIR / "data" / "scraped_data_async_improved.csv"
    output_path = BASE_DIR / "data" / "company_profiles_for_api.csv"
    merge_for_api_input(
        scraped_path,
        names_path,
        output_path
    )
