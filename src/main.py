import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from config.settings import (
    DATAFORSEO_USERNAME, DATAFORSEO_PASSWORD, DATAFORSEO_DOMAIN,
    LOCATION_CSV_PATH, LANGUAGE_CSV_PATH,
    MAX_WORKERS, TOP_KEYWORDS_COUNT, MAX_COMPETITORS, OPENAI_API_KEY
)
from src.api.rest_client import RestClient
from src.api.serp_fetcher import SerpFetcher
from src.api.content_summary_fetcher import ContentSummaryFetcher
from src.utils.url_processor import URLProcessor
from src.analysis.keyword_density_analyzer import KeywordDensityAnalyzer
from src.analysis.gpt_brief_generator import GPTBriefGenerator
from src.utils.csv_handler import CSVHandler
from src.utils.url_similarity import URLSimilarityAnalyzer

def get_user_choice(options, prompt):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("Enter your choice (number): ")) - 1
            if 0 <= choice < len(options):
                return options[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    # Initialize clients and handlers
    client = RestClient(DATAFORSEO_USERNAME, DATAFORSEO_PASSWORD, DATAFORSEO_DOMAIN)
    serp_fetcher = SerpFetcher(client)
    content_summary_fetcher = ContentSummaryFetcher(client)
    gpt_brief_generator = GPTBriefGenerator()
    keyword_density_analyzer = KeywordDensityAnalyzer()
    csv_handler = CSVHandler()
    url_processor = URLProcessor(client, DATAFORSEO_USERNAME, DATAFORSEO_PASSWORD)
    url_analyzer = URLSimilarityAnalyzer(OPENAI_API_KEY)

    # Load CSV data
    csv_handler.load_csv(LOCATION_CSV_PATH, 'location')
    csv_handler.load_csv(LANGUAGE_CSV_PATH, 'language')

    # Get user input
    keyword = input("Enter the keyword to analyze: ")
    reference_url = input("Enter a reference URL (optional, press Enter to skip): ").strip() or None
    
    # Get user input for link building opportunities
    include_outlinks = input("\nDo you want to include potential outlink suggestions in the brief? (y/n): ").lower() == 'y'

    potential_outlinks = None
    if include_outlinks:
        # Get user input for database
        available_dbs = url_analyzer.get_available_databases()
        selected_db = get_user_choice(available_dbs, "\nAvailable databases for potential outlinks:")
        
        # Get user input for cluster
        available_clusters = url_analyzer.get_clusters_for_database(selected_db)
        cluster_options = available_clusters + ["All clusters"]
        selected_cluster = get_user_choice(cluster_options, "\nAvailable clusters:")
        cluster_name = None if selected_cluster == "All clusters" else selected_cluster

        # Get user input for hard clustering
        hard_clustering = input("Enable hard clustering? (y/n): ").lower() == 'y'

    # Get user input for location and language
    selected_location, location_code = csv_handler.get_user_choice('location')
    selected_language, language_code = csv_handler.get_user_choice('language')

    print(f"\nSelected location: {selected_location}")
    print(f"Selected language: {selected_language}")
    if reference_url:
        print(f"Reference URL: {reference_url}")

    # Fetch SERP results
    print("\nFetching SERP results...")
    serp_results = serp_fetcher.get_serp_results(keyword, language_code, location_code)
    if not serp_results:
        print("Failed to fetch SERP results. Exiting.")
        return

    # Fetch content summary
    print("Fetching content summary...")
    time.sleep(5)
    content_summary = content_summary_fetcher.get_content_summary(serp_results['id'])
    if content_summary is None:
        print("Failed to fetch content summary. Exiting.")
        return
        

    # Process URLs
    print("Processing URLs...")
    urls_to_process = [result['url'] for result in serp_results['result'][0]['items'][:MAX_COMPETITORS] if result['type'] == 'organic']
    if reference_url:
        urls_to_process.append(reference_url)

    compiled_data = process_urls(url_processor, urls_to_process, keyword)
    compiled_data['content_summary'] = content_summary[0]['summary'] if content_summary else ""

    # Analyze keywords
    print("Analyzing keywords...")
    all_keywords = analyze_keywords(keyword_density_analyzer, compiled_data, keyword)

    # Extract reference data if it exists
    reference_data = next((data for data in compiled_data['detailed_analysis'] if data['url'] == reference_url), None)

    if include_outlinks:
        print("\nFinding potential outlinks...")
        potential_outlinks = url_analyzer.find_potential_outlinks(
            keyword,
            selected_db, 
            cluster_name, 
            hard_clustering=hard_clustering
        )
        print("Potential outlinks found:", potential_outlinks)

    # Generate brief
    print("\nGenerating brief...")
    brief = gpt_brief_generator.generate_brief(
        keyword, 
        compiled_data, 
        all_keywords[:TOP_KEYWORDS_COUNT], 
        potential_outlinks,
        reference_data, 
        selected_language
    )

    print("\nSEO Content Brief:")
    print(brief)

def process_urls(url_processor, urls, keyword):
    compiled_data = {
        'top_competitors': [],
        'detailed_analysis': [],
        'content_outline': "",
        'avg_image_count': 0
    }
    all_keywords = []
    image_counts = []
    word_counts = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(url_processor.process_url, keyword, url): url for url in urls}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                url_data = future.result()
                if url_data:
                    compiled_data['top_competitors'].append(f"{url_data['url']}")
                    compiled_data['detailed_analysis'].append(url_data)
                    all_keywords.extend(url_data.get('all_keywords', []))
                    image_counts.append(url_data.get('images_count', 0))
                    word_counts.append(url_data.get('plain_text_word_count', 0))
                else:
                    print(f"No data returned for URL: {url}")
            except Exception as e:
                print(f"Error processing URL {url}: {str(e)}")

    compiled_data['content_outline'] = generate_content_outline(compiled_data['detailed_analysis'])
    compiled_data['avg_image_count'] = sum(image_counts) / len(image_counts) if image_counts else 0
    return compiled_data

def analyze_keywords(keyword_density_analyzer, compiled_data, target_keyword):
    all_keywords = [kw for analysis in compiled_data['detailed_analysis'] for kw in analysis['all_keywords']]
    all_keywords = list({kw['keyword']: kw for kw in all_keywords}.values())  # Remove duplicates

    keywords = [kw['keyword'] for kw in all_keywords]
    print("Calculating keyword similarities...")
    try:
        similarities = keyword_density_analyzer.calculate_similarity(keywords, target_keyword)
        for kw, sim in zip(all_keywords, similarities):
            kw['similarity'] = sim
        all_keywords.sort(key=lambda x: (x['similarity'], x['frequency']), reverse=True)
    except Exception as e:
        print(f"Error calculating similarities: {e}")
        print("Proceeding with sorting based on frequency only.")
        all_keywords.sort(key=lambda x: x['frequency'], reverse=True)

    print("\nTop Keywords:")
    for i, kw in enumerate(all_keywords[:TOP_KEYWORDS_COUNT], 1):
        similarity = kw.get('similarity', 'N/A')
        similarity_str = f"{similarity:.2f}" if isinstance(similarity, float) else similarity
        print(f"{i}. {kw['keyword']} (Similarity: {similarity_str}, Frequency: {kw['frequency']})")

    return all_keywords

def generate_content_outline(detailed_analysis):
    content_outline = []
    for analysis in detailed_analysis:
        content_outline.append(f"URL: {analysis['url']}")
        headings = analysis.get('headings', {})
        if headings:
            for tag, heading_list in headings.items():
                if heading_list:
                    for heading in heading_list:
                        content_outline.append(f"{tag.upper()}: {heading}")
        else:
            content_outline.append("No headings found for this URL")
    return "\n".join(content_outline)

if __name__ == "__main__":
    main()