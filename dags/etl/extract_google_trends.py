import time
import requests
import concurrent.futures
import pandas as pd
import os

API_TOKEN = "apify_api_XFZhJOWDOXZfankLvHRWPJ3VeGpcsB46RA1g"  # Ganti dengan token API Anda
ACTOR_ID = "DyNQEYDj9awfGQf9A"  # Ganti dengan ID actor Anda
SEARCH_TERMS_LIST = ["sunscreen Azarine", "sunscreen Skin Aqua"]  # Ganti dengan kata kunci pencarian Anda
OUTPUT_DIR = "dags/hasil data extract"  # Ganti dengan direktori output yang diinginkan

def run_actor_for_term(term, api_token, actor_id):
    """
    Menjalankan actor Apify untuk satu kata kunci dan memeriksa statusnya.
    """
    # Siapkan input untuk actor
    run_input = {
        "searchTerms": [term],
        "isMultiple": False,
        "timeRange": "today 3-m",
        "viewedFrom": "id",  # Kode negara Indonesia
        "geo": "ID",
        "skipDebugScreen": False,
        "isPublic": False,
        "maxItems": 0,
        "maxConcurrency": 10,
        "maxRequestRetries": 7,
        "pageLoadTimeoutSecs": 180,
    }

    # Jalankan Actor
    print(f"Menjalankan Actor di Apify untuk '{term}'...")
    run_url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={api_token}"
    response = requests.post(run_url, json=run_input)
    
    if response.status_code != 201:
        print(f"Error menjalankan Actor: {response.status_code} - {response.text}")
        return None
    
    run_data = response.json()
    run_id = run_data['data']['id']
    print(f"Actor dijalankan dengan run_id: {run_id}")

    # Tunggu hingga Actor selesai
    wait_for_actor_to_finish(run_id, api_token)

    # Ambil hasil dataset
    dataset_id = run_data['data']['defaultDatasetId']
    dataset_results = get_dataset_results(dataset_id, api_token)

    if dataset_results:
        print(f"Found {len(dataset_results)} items in dataset for '{term}'.")
        save_results_to_csv(dataset_results, term)

def check_actor_status(run_id, api_token):
    """
    Memeriksa status actor berdasarkan run_id.
    """
    status_url = f"https://api.apify.com/v2/runs/{run_id}?token={api_token}"
    response = requests.get(status_url)
    if response.status_code == 200:
        run_data = response.json()
        return run_data['data']['status'], run_data['data']['finishedAt']
    else:
        print(f"Error checking status: {response.status_code} - {response.text}")
        return None, None

def wait_for_actor_to_finish(run_id, api_token):
    """
    Menunggu hingga actor selesai, memeriksa status setiap 30 detik.
    """
    while True:
        status, finished_at = check_actor_status(run_id, api_token)
        if status == 'SUCCEEDED':
            print("Actor completed successfully.")
            return
        elif status == 'FAILED':
            print("Actor failed.")
            return
        elif status == 'READY':
            print("Actor is still in progress...")
        else:
            print(f"Unknown status: {status}")
        
        # Tunggu 30 detik sebelum memeriksa lagi
        time.sleep(30)

def get_dataset_results(dataset_id, api_token):
    """
    Mengambil hasil dari dataset setelah actor selesai.
    """
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={api_token}"
    response = requests.get(dataset_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching dataset: {response.status_code} - {response.text}")
        return None

def save_results_to_csv(results, search_term):
    """
    Menyimpan hasil ke file CSV.
    """
    # Buat DataFrame dari hasil
    df = pd.DataFrame(results)

    # Sanitasi nama file
    sanitized_term = search_term.replace(" ", "_")
    filename = f"GoogleTrends_{sanitized_term}.csv"
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Simpan ke CSV
    print(f"Menyimpan data ke {output_path}...")
    df.to_csv(output_path, index=False)

def extract_google_trends():
    # Jalankan proses scraping untuk setiap kata kunci secara paralel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda term: run_actor_for_term(term, API_TOKEN, ACTOR_ID), SEARCH_TERMS_LIST)

if __name__ == "__main__":
    extract_google_trends()
