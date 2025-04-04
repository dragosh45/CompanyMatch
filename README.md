# Company Scraper & Matcher

This project scrapes data from company websites, indexes it in Elasticsearch, and exposes a FastAPI endpoint for fuzzy matching company profiles.

---

## 📁 Project Structure

```
.
├── crawler_p1.py                     # Initial synchronous web crawler
├── crawler_p2.py                     # Async version with concurrency
├── crawler_p2_improved.py            # Improved async crawler
├── crawler_p2_improved_fallback.py   # Adds fallback logic to scraper
├── merge_to_api_format.py            # Merges raw scraped data to API format
├── index_api_input_format.py         # Indexes formatted data to Elasticsearch
├── final_company_match_api.py        # FastAPI service for fuzzy matching
├── test_api_batch.py                 # Batch test the API endpoint
├── analyze.py                        # Analysis and reporting
├── run_main.py                       # Main pipeline controller
├── requirements.txt                  # Dependencies list
└── *.csv                             # Input/output data files
```

---

## 🧠 Matching Algorithm

The matching endpoint uses **RapidFuzz** to compute similarity scores between input data and existing company profiles. Each field has a weight:

- **Name**: 40%
- **Website**: 30%
- **Phone**: 20%
- **Facebook**: 10%

The company with the highest total weighted score is returned as the best match.

---

## ⚙️ How to Run

### 1. Set up Elasticsearch

Run Elasticsearch in Docker:

```bash
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.6.2
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the pipeline step-by-step

```bash
python crawler_p2_improved_fallback.py     # Scrape websites
python merge_to_api_format.py              # Merge into API format
python index_api_input_format.py           # Index into Elasticsearch
uvicorn final_company_match_api:app --reload   # Start FastAPI
python test_api_batch.py                   # Batch test API with input CSV
```

### 4. Optional: Analyze Results

```bash
python analyze.py
```

---

## 📌 CSV File Descriptions

- `scraped_data_async_improved.csv`: Raw scraped data
- `API-input-sample.csv`: Companies to match via API
- `api_matching_results.csv`: Output results from the matcher

---

## ✅ Features

- Async scraping with retry logic and fallback
- Elasticsearch indexing and querying
- FastAPI endpoint for fuzzy matching
- Docker support for local Elasticsearch

---

## 🧪 Testing

You can test the FastAPI using `curl` or Postman:

```bash
curl -X POST "http://127.0.0.1:8000/match" -H "Content-Type: application/json" -d '{"name": "Example Corp", "website": "example.com"}'
```

---

