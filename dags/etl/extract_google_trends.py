import os
import requests
import csv
import json
import logging
import time
import ast

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_actor(api_token, actor_id, actor_input):
    url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={api_token}"
    try:
        response = requests.post(url, json=actor_input, headers={"Content-Type": "application/json"})
        logging.info(f"Sent request to Apify API to run actor with status code: {response.status_code}")
        if response.status_code == 201:
            return response.json()["data"]["id"]  # Return the run ID
        else:
            logging.error(f"Error starting actor run: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return None

def get_actor_run_status(api_token, run_id):
    url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={api_token}"
    try:
        response = requests.get(url)
        logging.info(f"Checked actor run status with status code: {response.status_code}")
        if response.status_code == 200:
            return response.json()["data"]["status"]  # Return the status of the run
        else:
            logging.error(f"Error fetching actor run status: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Exception occurred while fetching run status: {e}")
        return None

def get_dataset(api_token, dataset_id):
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={api_token}"
    try:
        response = requests.get(url)
        logging.info(f"Fetched dataset with status code: {response.status_code}")
        if response.status_code == 200:
            return response.json()  # Return the dataset
        else:
            logging.error(f"Error fetching dataset: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return None

def scrape_and_process_apify(api_token, actor_id, search_terms, output_folder):
    for term in search_terms:
        logging.info(f"Running Apify actor for '{term}'...")

        run_input = {
            "searchTerms": [term],
            "isMultiple": False,
            "timeRange": "today 3-m",
            "viewedFrom": "id",  # Country code: "id" for Indonesia
            "geo": "ID",
            "skipDebugScreen": False,
            "isPublic": False,
            "maxItems": 0,
            "maxConcurrency": 10,
            "maxRequestRetries": 7,
            "pageLoadTimeoutSecs": 180,
        }

        # Run the actor and get the run ID
        run_id = run_actor(api_token, actor_id, run_input)
        if not run_id:
            logging.warning(f"Failed to start actor run for '{term}'.")
            continue

        # Polling the actor run status until it finishes
        status = None
        while status not in ["SUCCEEDED", "FAILED"]:
            status = get_actor_run_status(api_token, run_id)
            if status == "FAILED":
                logging.error(f"Actor run failed for '{term}'.")
                break
            elif status == "SUCCEEDED":
                logging.info(f"Actor run succeeded for '{term}'.")
            else:
                logging.info(f"Actor is still running for '{term}'... Waiting...")
                time.sleep(10)  # Wait before checking the status again

        if status == "SUCCEEDED":
            # Once the actor run is complete, retrieve the dataset
            dataset_id = "WIQtOSEKdt30fyUab"  # Replace with the actual dataset ID
            dataset = get_dataset(api_token, dataset_id)

            if dataset:
                term_filename = term.replace(" ", "_")
                json_filename = os.path.join(output_folder, f"GoogleTrend_{term_filename}.json")
                csv_filename = os.path.join(output_folder, f"GoogleTrend_{term_filename}_interestOverTime.csv")

                # Save results to JSON file
                with open(json_filename, "w") as json_file:
                    json.dump(dataset, json_file, indent=4)
                logging.info(f"Data for '{term}' saved to '{json_filename}'.")

                # Extract and process 'interestOverTime_timelineData' column
                timeline_data_parsed = []

                for row in dataset:
                    timeline_data = row.get("interestOverTime_timelineData")
                    if timeline_data:
                        try:
                            parsed_data = ast.literal_eval(timeline_data) if isinstance(timeline_data, str) else timeline_data
                            timeline_data_parsed.extend(parsed_data)
                        except (ValueError, SyntaxError) as e:
                            logging.error(f"Error processing row: {e}, data: {timeline_data}")
                            continue

                # Save the processed data to CSV
                if timeline_data_parsed:
                    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
                        csv_writer = csv.writer(csvfile)
                        # Write header based on the structure of the first entry
                        if timeline_data_parsed:
                            headers = timeline_data_parsed[0].keys()
                            csv_writer.writerow(headers)
                            # Write each row
                            for data in timeline_data_parsed:
                                csv_writer.writerow(data.values())

                    logging.info(f"Interest over time data for '{term}' saved to '{csv_filename}'.")
                else:
                    logging.warning(f"No data found for 'interestOverTime_timelineData' for '{term}'.")

def extract_google_trends():
    api_token = "api token"  # Replace with your API token
    actor_id = "emastra~google-trends-scraper"  # Replace with your Apify Actor ID
    search_terms = ["sunscreen skin aqua", "sunscreen Azarine"]
    output_folder = "dags/hasil data extract"

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    logging.info("Starting Google Trends data scraping...")
    scrape_and_process_apify(api_token=api_token, actor_id=actor_id, search_terms=search_terms, output_folder=output_folder)
    logging.info("Google Trends data scraping completed.")

# Example usage
if __name__ == "__main__":
    extract_google_trends()
