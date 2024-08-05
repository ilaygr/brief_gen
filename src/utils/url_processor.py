import time
from nltk.corpus import stopwords
from src.utils.url_parser import parse_url

stop_words = set(stopwords.words('english'))

class URLProcessor:
    def __init__(self, client, username, password):
        self.client = client
        self.username = username
        self.password = password

    def process_url(self, keyword, url):
        page_details = self.get_on_page_data(url)
        if not page_details:
            return None

        task_id = self.create_onpage_task(url)
        if not task_id:
            return None

        print(f"Waiting for 35 seconds before fetching keyword density for {url}....")
        time.sleep(35)

        keyword_density_list = self.get_keyword_density(task_id, url)
        if not keyword_density_list:
            return None

        all_items = []
        for keyword_density in keyword_density_list:
            if keyword_density.get('items'):
                all_items.extend(keyword_density['items'])

        if not all_items:
            print(f"No keyword items found for {url}.")
            return None

        relevant_keywords = [
            {**kw, 'similarity': 0}  # Initialize similarity to 0, will be calculated later
            for kw in all_items
            if kw['keyword'] not in stop_words
        ]
        relevant_keywords.sort(key=lambda x: x['frequency'], reverse=True)

        return {
            'url': url,
            'headings': page_details['headings'],
            'images_count': page_details['images_count'],
            'plain_text_word_count': page_details['plain_text_word_count'],
            'relevant_keywords': relevant_keywords[:10],
            'all_keywords': relevant_keywords
        }

    def get_on_page_data(self, url):
        post_data = {
            str(int(time.time())): {
                "url": url,
                "enable_javascript": False
            }
        }
        response = self.client.post("/v3/on_page/instant_pages", post_data)
        
        if response["status_code"] == 20000:
            try:
                tasks = response.get("tasks", [])
                if tasks and isinstance(tasks[0].get("result"), list) and tasks[0]["result"]:
                    item = tasks[0]["result"][0].get("items", [{}])[0]
                    return {
                        "url": item.get("url", url),
                        "headings": item.get("meta", {}).get("htags", {}),
                        "images_count": item.get("meta", {}).get("images_count", 0),
                        "plain_text_word_count": item.get("meta", {}).get("content", {}).get("plain_text_word_count", 0)
                    }
                else:
                    print(f"No valid data found in the response for URL: {url}")
                    return None
            except (KeyError, IndexError) as e:
                print(f"Error extracting data: {e}")
                return None
        else:
            print(f"Error. Code: {response['status_code']} Message: {response.get('status_message', 'Unknown error')}")
            return None

    def create_onpage_task(self, url):
        domain, full_url = parse_url(url)
        task_id = str(int(time.time()))
        post_data = {
            task_id: {
                "target": domain,
                "max_crawl_pages": 1,
                "start_url": full_url,
                "load_resources": False,
                "enable_javascript": False,
                "calculate_keyword_density": True,
                "respect_robots_txt": True,
                "custom_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        }

        response = self.client.post("/v3/on_page/task_post", post_data)
        print("On-Page Task Response:", response)

        if response["status_code"] == 20000 and 'tasks' in response and len(response['tasks']) > 0:
            task_id = response['tasks'][0]['id']
            print("Task ID:", task_id)
            return task_id
        else:
            print(f"Error creating task. Code: {response['status_code']} Message: {response['status_message']}")
            return None

    def get_keyword_density(self, task_id, url, retries=5, delay=35):
        all_results = []
        for keyword_length in range(1, 5):  # 1, 2, 3, 4
            for attempt in range(retries):
                post_data = {
                    0: {
                        "id": task_id,
                        "url": url,
                        "keyword_length": keyword_length,
                        "filters": ["frequency", ">", 5]
                    }
                }

                response = self.client.post("/v3/on_page/keyword_density", post_data)
                print(f"Attempt {attempt + 1} for keyword length {keyword_length}: Keyword Density Response:", response)

                if response["status_code"] == 20000:
                    if 'tasks' in response and len(response['tasks']) > 0:
                        result = response['tasks'][0].get('result')
                        if result:
                            all_results.extend(result)
                            break  # Success, move to next keyword length
                        else:
                            print(f"No results found for keyword length {keyword_length}. The task might still be processing.")
                    else:
                        print(f"No tasks found in the response for keyword length {keyword_length}.")
                elif response["status_code"] == 40400:  # Not Found error
                    print(f"Task not ready yet for keyword length {keyword_length}. Waiting {delay} seconds before retry...")
                else:
                    print(f"Error for keyword length {keyword_length}. Code: {response['status_code']} Message: {response['status_message']}")
                
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
            else:
                print(f"Max retries reached for keyword length {keyword_length}. Could not retrieve keyword density data.")
        
        return all_results if all_results else None