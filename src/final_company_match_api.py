from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from elasticsearch import Elasticsearch
from rapidfuzz import fuzz

app = FastAPI()
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "companies"

# Input model expected by the API
class CompanyInput(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    facebook: Optional[str] = None

# Matching function with weights
def compute_weighted_score(doc, input_data: CompanyInput):
    weights = {
        "input name": 0.4,
        "input website": 0.3,
        "input phone": 0.2,
        "input_facebook": 0.1
    }

    score = 0
    if input_data.name and doc.get("input name"):
        score += weights["input name"] * fuzz.token_sort_ratio(input_data.name, doc["input name"])
    if input_data.website and doc.get("input website"):
        score += weights["input website"] * fuzz.token_sort_ratio(input_data.website, doc["input website"])
    if input_data.phone and doc.get("input phone"):
        score += weights["input phone"] * fuzz.token_sort_ratio(input_data.phone, doc["input phone"])
    if input_data.facebook and doc.get("input_facebook"):
        score += weights["input_facebook"] * fuzz.token_sort_ratio(input_data.facebook, doc["input_facebook"])

    return score

# Main API endpoint for matching
@app.post("/match")
def match_company(input_data: CompanyInput):
    resp = es.search(index=INDEX_NAME, body={"query": {"match_all": {}}}, size=1000)
    companies = [hit["_source"] for hit in resp["hits"]["hits"]]

    best_score = -1
    best_match = None

    for company in companies:
        score = compute_weighted_score(company, input_data)
        if score > best_score:
            best_score = score
            best_match = company

    return {
        "input": input_data.dict(),
        "best_score": round(best_score, 2),
        "best_match": best_match
    }
