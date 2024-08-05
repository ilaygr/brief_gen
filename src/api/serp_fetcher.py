from config.settings import MAX_RETRIES, RETRY_DELAY
import time

class SerpFetcher:
    def __init__(self, client):
        self.client = client

    def get_serp_results(self, keyword, language_code, location_code):
        print("Step 1 - Fetching SERP results....")
        post_data = {
            0: {
                "language_code": language_code,
                "location_code": location_code,
                "keyword": keyword,
                "calculate_rectangles": True
            }
        }
        
        for attempt in range(MAX_RETRIES):
            response = self.client.post("/v3/serp/google/organic/live/advanced", post_data)
            if response["status_code"] == 20000:
                print("SERP results fetched successfully.")
                return response["tasks"][0]
            elif response["status_code"] == 40400:
                print(f"Task not ready yet. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Error fetching SERP results. Code: {response['status_code']} Message: {response['status_message']}")
                return None
        
        print("Max retries reached. Failed to fetch SERP results.")
        return None