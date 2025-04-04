from pathlib import Path

import pandas as pd
from elasticsearch import Elasticsearch, helpers

# Elasticsearch setup
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "companies"

def index_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    input_file = BASE_DIR / "data" / "company_profiles_for_api.csv"
    df = pd.read_csv(input_file).fillna("")

    documents = []
    for _, row in df.iterrows():
        doc = {
            "input name": row.get("input name", ""),
            "input phone": row.get("input phone", ""),
            "input website": row.get("input website", ""),
            "input_facebook": row.get("input_facebook", "")
        }
        documents.append(doc)

    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
    es.indices.create(index=INDEX_NAME)

    actions = [
        {"_index": INDEX_NAME, "_source": doc}
        for doc in documents
    ]
    helpers.bulk(es, actions)
    print(f"-----> Indexed {len(actions)} documents into '{INDEX_NAME}'.")

if __name__ == "__main__":
    index_data()
