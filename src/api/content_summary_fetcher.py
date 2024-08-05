class ContentSummaryFetcher:
    def __init__(self, client):
        self.client = client

    def get_content_summary(self, task_id, prompt="Provide a summary of the SERP results", include_links=True, fetch_content=True, support_extra=False):
        print("Step 2 - Creating AI summary....")
        post_data = {
            0: {
                "task_id": task_id,
                "prompt": prompt,
                "include_links": include_links,
                "fetch_content": fetch_content,
                "support_extra": support_extra
            }
        }
        response = self.client.post("/v3/serp/ai_summary", post_data)
        
        if response["status_code"] == 20000:
            print("AI summary request successful.")
            if "tasks" in response and response["tasks"]:
                task = response["tasks"][0]
                if "result" in task and task["result"]:
                    if isinstance(task["result"], list) and task["result"] and "items" in task["result"][0]:
                        print("AI summary created successfully.")
                        return task["result"][0]["items"]
                    else:
                        print("Unexpected result structure. Full task result:", task["result"])
                else:
                    print("Task result is empty or not available yet.")
            else:
                print("No tasks found in the response.")
        else:
            print(f"Error fetching content summary. Code: {response['status_code']} Message: {response.get('status_message', 'Unknown error')}")
        
        print("Full API response:", response)
        return None