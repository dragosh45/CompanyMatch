from pathlib import Path

import pandas as pd
import requests
import time

API_URL = "http://localhost:8000/match"
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "API-input-sample.csv"
OUTPUT_FILE = BASE_DIR / "data" / "api_matching_results.csv"

def test_api_and_save_results():
    df = pd.read_csv(INPUT_FILE).fillna("")
    results = []

    for idx, row in df.iterrows():
        payload = {
            "name": row.get("input name", ""),
            "website": row.get("input website", ""),
            "phone": row.get("input phone", ""),
            "facebook": row.get("input_facebook", "")
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                best_match = data.get("best_match", {})
                score = data.get("best_score", 0)
                result_row = {
                    "input name": payload["name"],
                    "input website": payload["website"],
                    "input phone": payload["phone"],
                    "input_facebook": payload["facebook"],
                    "matched name": best_match.get("input name", ""),
                    "matched website": best_match.get("input website", ""),
                    "matched phone": best_match.get("input phone", ""),
                    "matched facebook": best_match.get("input_facebook", ""),
                    "score": score
                }
                results.append(result_row)
            else:
                print(f"******> Error for row {idx}, status: {response.status_code}")
        except Exception as e:
            print(f"******> Exception on row {idx}: {e}")
        time.sleep(0.1)  # small delay to avoid overwhelming server

    pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
    print(f"------> Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    test_api_and_save_results()
