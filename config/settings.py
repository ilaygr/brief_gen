import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# API credentials
DATAFORSEO_USERNAME = os.getenv('DATAFORSEO_USERNAME', 'your_default_username')
DATAFORSEO_PASSWORD = os.getenv('DATAFORSEO_PASSWORD', 'your_default_password')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_default_openai_key')

# API settings
DATAFORSEO_DOMAIN = "api.dataforseo.com"
MAX_RETRIES = 5
RETRY_DELAY = 35

# Analysis settings
MAX_COMPETITORS = 10
TOP_KEYWORDS_COUNT = 40
SIMILARITY_THRESHOLD = 0.6
MAX_LINK_SUGGESTIONS = 5

# Threading
MAX_WORKERS = 5

# Model settings
GPT_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-ada-002"

# CSV file paths
LOCATION_CSV_PATH = os.path.join(DATA_DIR, 'Country_List - Sheet1.csv')
LANGUAGE_CSV_PATH = os.path.join(DATA_DIR, 'languages_serp_google_2023_05_02.csv')

# URL databases directory
URL_DATABASES_DIR = os.path.join(DATA_DIR, 'url_databases')
os.makedirs(URL_DATABASES_DIR, exist_ok=True)

# Linking opportunities limit
MAX_POTENTIAL_OUTLINKS = 10

# Dictionary to store paths of all URL database CSV files
URL_DATABASES = {os.path.splitext(f)[0]: os.path.join(URL_DATABASES_DIR, f) 
                 for f in os.listdir(URL_DATABASES_DIR) if f.endswith('.csv')}