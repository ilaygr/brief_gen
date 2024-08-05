# TODO List

## 1. Export to Google Doc
- [ ] Set up Google Drive API credentials
- [ ] Create a new class `GoogleDocExporter`:
  - [ ] Implement method to authenticate with Google Drive API
  - [ ] Implement method to create a new Google Doc
  - [ ] Implement method to write content to the Google Doc
  - [ ] Implement method to format the document (headings, lists, etc.)
- [ ] Update `main.py` to include option for Google Doc export
- [ ] Handle errors and exceptions for API interactions

## 2. Generate Article based on Brief
- [ ] Create a new class `ArticleGenerator`:
  - [ ] Implement method to create a prompt for article generation
  - [ ] Implement method to interact with OpenAI API for content generation
  - [ ] Implement method to structure the generated content according to the brief
- [ ] Create a dedicated prompt for article generation
- [ ] Update `main.py` to include option for article generation
- [ ] Handle API rate limits and implement retries

## 3. Localize Article based on Brief
- [ ] Create a new class `ArticleLocalizer`:
  - [ ] Implement method to create a prompt for article localization
  - [ ] Implement method to interact with OpenAI API for content localization
  - [ ] Implement method to adapt content structure for the target language
- [ ] Create a dedicated prompt for article localization
- [ ] Update `main.py` to include option for article localization
- [ ] Implement language detection to ensure source and target languages are different

## 4. New Logic of Broad Inlinks Strategy
- [ ] Create a new class `BroadInlinkAnalyzer`:
  - [ ] Implement method to crawl each database
  - [ ] Implement method to calculate semantic similarity between h1/content
  - [ ] Implement method to check existing links and cluster information
  - [ ] Implement method to generate inlink recommendations
- [ ] Update `URLSimilarityAnalyzer` class to incorporate new broad inlink logic
- [ ] Create a dedicated prompt for inlink recommendations
- [ ] Update `main.py` to include option for broad inlink analysis

## 5. Product Page Linking
- [ ] Add product page logic to the database
- [ ] Add option to choose one or more product pages to suggest links
- [ ] Allow option for automated choice based on top similar articles

## 6. Build UI in Streamlit
- [ ] Set up Streamlit in the project
- [ ] Create a new file `app.py` for the Streamlit application
- [ ] Implement UI components:
  - [ ] Input fields for keyword, reference URL, etc.
  - [ ] Dropdown menus for database and cluster selection
  - [ ] Buttons for different actions (generate brief, export to Google Doc, etc.)
  - [ ] Display area for the generated brief and other outputs
- [ ] Integrate existing functionality with the Streamlit UI
- [ ] Implement error handling and user feedback in the UI

## 7. Higher Number of Links Suggestions
- [ ] Increase the number of link suggestions in the recommendation logic

## 8. Multiple Clustering Choices
- [ ] Allow multiple clustering choices in addition to the option to choose all
- [ ] Remove hard/soft clustering logic as it is no longer relevant

## 9. Dynamic Prompt Templates
- [ ] Build dynamic prompt templates injected with different prompt parts based on user choices and app logic
- [ ] Allow content format brief:
  - [ ] Write different prompts for different content types (review, how-to, branded, case study, more...)
  - [ ] Add option to include {Brand} and adjust the prompts to focus on this brand and not on competitors when crafting the brief (mainly outline and related words)

## 10. Refactor Code
- [ ] Implement caching:
  - [ ] Use `functools.lru_cache` for frequently called functions
  - [ ] Implement disk-based caching for API responses
- [ ] Improve error handling:
  - [ ] Create a custom `Exception` class for project-specific errors
  - [ ] Implement try-except blocks in all API interactions and file operations
  - [ ] Create meaningful error messages for users
- [ ] Enhance modularity:
  - [ ] Break down large functions into smaller, more focused functions
  - [ ] Use dependency injection where appropriate
- [ ] Improve readability:
  - [ ] Add comprehensive docstrings to all classes and methods
  - [ ] Follow PEP 8 style guide consistently
  - [ ] Use type hints throughout the codebase
- [ ] Increase maintainability:
  - [ ] Create a `config.py` file for all configuration variables
  - [ ] Implement logging throughout the application
  - [ ] Write unit tests for all new and refactored components
- [ ] Create a `requirements.txt` file with all project dependencies
- [ ] Update `README.md` with setup instructions and usage examples
