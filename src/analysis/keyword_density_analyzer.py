from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config.settings import OPENAI_API_KEY
from tqdm import tqdm
import time

class KeywordDensityAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "text-embedding-3-large"

    def get_embedding(self, text):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.embeddings.create(
                    input=text,
                    model=self.model
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"Error getting embedding for '{text}': {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in 5 seconds... (Attempt {attempt + 2}/{max_retries})")
                    time.sleep(5)
                else:
                    print(f"Failed to get embedding for '{text}' after {max_retries} attempts.")
                    return None

    def calculate_similarity(self, keywords, target_keyword):
        print(f"Calculating similarity for {len(keywords)} keywords...")
        target_embedding = self.get_embedding(target_keyword)
        if target_embedding is None:
            raise ValueError(f"Failed to get embedding for target keyword: {target_keyword}")

        keyword_embeddings = []
        for keyword in tqdm(keywords, desc="Getting embeddings", unit="keyword"):
            embedding = self.get_embedding(keyword)
            if embedding is not None:
                keyword_embeddings.append(embedding)
            else:
                print(f"Skipping keyword '{keyword}' due to embedding failure.")

        if not keyword_embeddings:
            raise ValueError("Failed to get embeddings for all keywords.")

        # Convert to numpy arrays for cosine_similarity function
        target_embedding = np.array(target_embedding).reshape(1, -1)
        keyword_embeddings = np.array(keyword_embeddings)

        similarities = cosine_similarity(target_embedding, keyword_embeddings)[0]
        return similarities