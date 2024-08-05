# SEO Content Brief Generator

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [API Integrations](#api-integrations)
9. [Data Flow](#data-flow)
10. [Key Components](#key-components)
11. [Error Handling](#error-handling)
12. [Performance Considerations](#performance-considerations)
13. [Future Enhancements](#future-enhancements)
14. [Troubleshooting](#troubleshooting)
15. [Contributing](#contributing)
16. [License](#license)

## Project Overview

The SEO Content Brief Generator is a sophisticated tool designed to streamline the process of creating comprehensive, data-driven SEO content briefs. By leveraging various APIs and advanced natural language processing techniques, this tool analyzes search engine results pages (SERPs), performs keyword density analysis, and generates actionable content briefs tailored to specific target keywords and audience needs.

## Features

- SERP analysis for target keywords
- Competitor content analysis
- Keyword density analysis
- AI-powered content summary generation
- Multilingual support
- Reference URL analysis
- Potential outlink suggestions
- GPT-powered brief generation
- Customizable content structure based on reference URLs
- Multithreaded URL processing for improved performance

## System Requirements

- Python 3.8+
- 8GB RAM (minimum)
- Internet connection for API access

## Project Structure

```
seo-content-brief-generator/
├── config/
│   ├── __init__.py
│   └── settings.py
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── content_summary_fetcher.py
│   │   ├── rest_client.py
│   │   └── serp_fetcher.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── gpt_brief_generator.py
│   │   └── keyword_density_analyzer.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── csv_handler.py
│   │   ├── url_parser.py
│   │   ├── url_processor.py
│   │   └── url_similarity.py
│   └── __init__.py
├── data/
│   ├── Country_List - Sheet1.csv
│   ├── languages_serp_google_2023_05_02.csv
│   └── url_databases/
│       └── [database CSV files]
├── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/seo-content-brief-generator.git
   cd seo-content-brief-generator
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the `config/settings.py.example` to `config/settings.py`:
   ```
   cp config/settings.py.example config/settings.py
   ```

2. Edit `config/settings.py` and add your API credentials:
   ```python
   DATAFORSEO_USERNAME = 'your_dataforseo_username'
   DATAFORSEO_PASSWORD = 'your_dataforseo_password'
   OPENAI_API_KEY = 'your_openai_api_key'
   ```

3. Adjust other settings in `config/settings.py` as needed, such as `MAX_COMPETITORS`, `TOP_KEYWORDS_COUNT`, etc.

## Usage

To run the SEO Content Brief Generator:

```
python main.py
```

Follow the interactive prompts to:
1. Enter the target keyword
2. Optionally provide a reference URL
3. Choose whether to include outlink suggestions
4. Select the target location and language
5. Wait for the analysis and brief generation to complete

The generated brief will be displayed in the console output.

## API Integrations

This project integrates with the following APIs:

1. DataForSEO API:
   - Used for SERP analysis, on-page data retrieval, and keyword density analysis
   - Endpoints used:
     - `/v3/serp/google/organic/live/advanced`
     - `/v3/on_page/instant_pages`
     - `/v3/on_page/task_post`
     - `/v3/on_page/keyword_density`
   - Rate limits apply, check DataForSEO documentation for details

2. OpenAI API:
   - Used for content summarization, keyword similarity analysis, and brief generation
   - Models used:
     - `text-embedding-3-large` for embeddings
     - `gpt-4o` for content generation
   - Rate limits apply, check OpenAI documentation for details

## Data Flow

1. User inputs target keyword and optional reference URL
2. SERP results are fetched for the target keyword
3. Content summary is generated from SERP results
4. Top competitor URLs are processed for on-page data and keyword density
5. Keyword similarity analysis is performed
6. If enabled, potential outlinks are identified from the URL database
7. All collected data is passed to the GPT brief generator
8. The generated brief is returned to the user

## Key Components

1. `SerpFetcher`: Retrieves SERP data from DataForSEO API
2. `ContentSummaryFetcher`: Generates AI-powered content summaries
3. `URLProcessor`: Handles on-page data retrieval and keyword density analysis
4. `KeywordDensityAnalyzer`: Performs keyword similarity analysis using OpenAI embeddings
5. `URLSimilarityAnalyzer`: Identifies potential outlinks based on semantic similarity
6. `GPTBriefGenerator`: Generates the final content brief using OpenAI's GPT model

## Error Handling

The application implements error handling for API requests, file operations, and user inputs. Common errors include:

- API connection failures
- Rate limit exceeded errors
- Invalid user inputs
- File not found errors

Error messages are displayed to the user with suggestions for resolution.

## Performance Considerations

- Multithreading is used for URL processing to improve performance
- API requests are retried with exponential backoff in case of failures
- Caching is implemented for embedding calculations to reduce API calls

## Future Enhancements

Refer to the `TODO.md` file for a list of planned enhancements, including:

- Export to Google Docs
- Article generation based on the brief
- Article localization
- Improved inlink strategy
- Streamlit UI implementation
- Dynamic prompt templates

## Troubleshooting

If you encounter issues:

1. Ensure all API credentials are correctly set in `config/settings.py`
2. Check your internet connection
3. Verify that you're not exceeding API rate limits
4. Ensure all required CSV files are present in the `data/` directory
5. Check the console output for specific error messages


Made by Ilay Granot
