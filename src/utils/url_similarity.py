import pandas as pd
import os
from typing import List, Dict, Optional
from config.settings import URL_DATABASES_DIR, MAX_POTENTIAL_OUTLINKS
from openai import OpenAI
import numpy as np

class URLSimilarityAnalyzer:
    def __init__(self, openai_api_key):
        self.databases = self._load_databases()
        self.client = OpenAI(api_key=openai_api_key)

    def _load_databases(self) -> Dict[str, pd.DataFrame]:
        databases = {}
        for filename in os.listdir(URL_DATABASES_DIR):
            if filename.endswith('.csv'):
                db_name = filename[:-4]  # Remove .csv extension
                file_path = os.path.join(URL_DATABASES_DIR, filename)
                databases[db_name] = pd.read_csv(file_path)
        print(f"Loaded databases: {list(databases.keys())}")
        return databases

    def get_available_databases(self) -> List[str]:
        return list(self.databases.keys())

    def get_clusters_for_database(self, db_name: str) -> List[str]:
        if db_name not in self.databases:
            print(f"Error: Database '{db_name}' not found.")
            return []
        return self.databases[db_name]['cluster_name'].unique().tolist()

    def find_potential_outlinks(self, target_keyword: str, db_name: str, cluster_name: Optional[str] = None, hard_clustering: bool = False) -> List[Dict[str, str]]:
        print(f"Finding potential outlinks for keyword '{target_keyword}' in database {db_name}")
        print(f"Cluster: {cluster_name}, Hard clustering: {hard_clustering}")

        if db_name not in self.databases:
            print(f"Error: Database '{db_name}' not found.")
            return []

        db_data = self.databases[db_name]
        
        if cluster_name and hard_clustering:
            db_data = db_data[db_data['cluster_name'] == cluster_name]
            print(f"Filtered to {len(db_data)} URLs in cluster {cluster_name}")

        target_embedding = self._get_embedding(target_keyword)
        similarities = []

        for _, row in db_data.iterrows():
            h1 = str(row['h1'])  # Ensure h1 is a string
            if pd.isna(h1) or h1 == '':
                print(f"Warning: Empty or NaN H1 for URL {row['url']}. Skipping.")
                continue
            h1_embedding = self._get_embedding(h1)
            similarity = self._calculate_similarity(target_embedding, h1_embedding)
            similarities.append({
                "url": row['url'],
                "similarity": similarity,
                "cluster": row['cluster_name'],
                "h1": h1
            })

        sorted_similarities = sorted(similarities, key=lambda x: x['similarity'], reverse=True)
        potential_outlinks = sorted_similarities[:MAX_POTENTIAL_OUTLINKS]

        print(f"Found {len(potential_outlinks)} potential outlinks")
        return potential_outlinks

    def _get_embedding(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(input=[text], model="text-embedding-ada-002")
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding for text: {text}")
            print(f"Error details: {str(e)}")
            return []

    def _calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        if not embedding1 or not embedding2:
            return 0.0
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))