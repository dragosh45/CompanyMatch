import subprocess
import time
import os
import sys
import requests

BASE_PATH = os.path.dirname(__file__)

def run_python_script(script_name):
    full_path = os.path.join(BASE_PATH, script_name)
    print(f"-------------- Running: {full_path}")
    subprocess.run([sys.executable, full_path], check=True)

def wait_for_api_ready(url="http://localhost:8000/docs", timeout=60):
    print(" Waiting for API to become available...")
    for _ in range(timeout):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                print("-----> API is ready.")
                return
        except:
            pass
        time.sleep(1)
    raise TimeoutError("*****> API did not become available in time.")

def main():
    print("[0/5] Starting Elasticsearch in Docker (or skipping if already running)...")
    subprocess.run([
        "docker", "start", "elasticsearch"
    ], stderr=subprocess.DEVNULL)
    subprocess.run([
        "docker", "run", "-d", "--name", "elasticsearch",
        "-p", "9200:9200", "-e", "discovery.type=single-node",
        "-e", "xpack.security.enabled=false",
        "docker.elastic.co/elasticsearch/elasticsearch:8.11.3"
    ], stderr=subprocess.DEVNULL)

    print("[1/5] Crawling company data...")
    run_python_script("crawler_p2_improved_fallback.py")
    run_python_script("analyze.py")

    print("[2/5] Merging scraped data with company names...")
    run_python_script("merge_to_api_format.py")

    print("[3/5] Indexing data to Elasticsearch...")
    run_python_script("index_api_input_format.py")

    print("[4/5] Starting FastAPI server in background...")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "final_company_match_api:app", "--reload"],
        cwd=BASE_PATH,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    wait_for_api_ready()

    print("[5/5] Running test API against input sample...")
    run_python_script("test_api_batch.py")

    print("------> All done.Check api_matching_results.csv")

if __name__ == "__main__":
    main()
