from openai import OpenAI
from config.settings import OPENAI_API_KEY, GPT_MODEL
import json

class GPTBriefGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_brief(self, keyword, compiled_data, top_keywords, potential_outlinks, reference_data=None, target_language=None):
        print("Generating brief with the following data:")
        print(f"Keyword: {keyword}")
        print(f"Target language: {target_language}")
        print(f"Potential outlinks: {potential_outlinks is not None}")
        print(f"Reference data: {reference_data is not None}")

        is_english = target_language.lower() in ['en', 'eng', 'english']
        keyword_strings = [kw['keyword'] for kw in top_keywords]
        
        prompt = self._create_prompt(keyword, compiled_data, keyword_strings, potential_outlinks, reference_data, target_language, is_english)

        is_english = target_language.lower() in ['en', 'eng', 'english']
        keyword_strings = [kw['keyword'] for kw in top_keywords]
        
        prompt = self._create_prompt(keyword, compiled_data, keyword_strings, potential_outlinks, reference_data, target_language, is_english)

        print("\nGenerating GPT Brief...")
        completion = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert SEO analyst specialized in creating comprehensive, actionable content briefs tailored to specific target keywords and audience needs. You excel at analyzing SERP data and reference content to inform content strategy."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

    def _create_prompt(self, keyword, compiled_data, top_keywords, potential_outlinks, reference_data, target_language, is_english):
        prompt = f"""
        Role: You are an expert SEO content strategist and translator tasked with creating a comprehensive and actionable content brief.

        Task: Create a detailed SEO Content Brief for the target keyword: "{keyword}"
        
        Critical Requirement: The content structure, target keyword, and related terms in your brief MUST be in the target language ({target_language}). All other sections should be in English.

        Input Data and Context:
        1. Target Keyword: "{keyword}"
           Context: This is the primary keyword the content should be optimized for.

        2. Target Language: {target_language}
           Context: This is the language for the content structure, target keyword, and related terms.

        3. SERP Summary:
           Context: This provides an overview of the current search engine results page for the target keyword and an analysis of the top 10 competitors.
           Data: 
           Overview: {compiled_data['content_summary']}
           Top 10 Competitors: {compiled_data['top_competitors']}

        4. Content Outline Based on Relevant Headings from the SERP:
           Context: This outline compiles important headings and subheadings from top-ranking pages. Use this to supplement the reference URL structure or create a new structure if no reference URL is provided.
           Data: {compiled_data['content_outline']}

        5. Related Keywords:
           Context: These are semantically related terms and phrases relevant to the target keyword. They should be incorporated into the content structure to improve topical relevance. Translate these to {target_language}.
           Data: {', '.join(top_keywords)}
        """

        if potential_outlinks:
            prompt += f"""
        6. Related Links:
           Context: These are specific relevant link sources that the new content could link to, enhancing its value and credibility. Only use these provided outlinks in your strategy.
           Data: {self._format_links(potential_outlinks)}
        """

        if reference_data:
            prompt += f"""
        7. Reference URL Data:
           Context: This is detailed information about a specific URL, including its headings and relevant keywords. This structure MUST be translated and used as the base for the content brief, supplemented with additional insights from the SERP data.
           Data:
           URL: {reference_data['url']}
           Headings: {json.dumps(reference_data['headings'], indent=2)}
           Relevant Keywords: {', '.join([kw['keyword'] for kw in reference_data['relevant_keywords']])}
        """

        prompt += f"""
        Instructions:
        Create a comprehensive SEO Content Brief using the following structure and guidelines:

        1. SERP Analysis (in English)
           - Provide a concise overview of the current SERP landscape based on the provided SERP summary.
           - Analyze the top 10 competitors, highlighting their main strengths and any notable weaknesses or content gaps.
           - Use bullet points for clarity and conciseness.

        2. Content Structure (in {target_language})
           - This section MUST present a single, coherent, detailed, hierarchical outline using proper heading tags (H1, H2, H3, H4).
           - The structure MUST incorporate insights from all provided data sources: reference URL (if available), SERP data, related keywords, key points, and unique angles.
           - If Reference URL data is provided:
             * Translate the entire heading structure from the Reference URL into {target_language}.
             * Maintain the exact heading hierarchy (H1, H2, H3, H4) from the Reference URL.
             * Supplement this structure with additional relevant headings from the SERP data, related keywords, key points, and unique angles.
             * Insert new headings where they fit most logically within the existing structure.
             * Clearly mark any added headings as [ADDED] to distinguish them from the original Reference URL structure.
           - If no Reference URL data is provided:
             * Create a comprehensive outline based on the SERP data, related keywords, key points, and unique angles.
             * Use H1 for the main title, H2 for main sections, H3 for subsections, and H4 for further breakdowns if necessary.
           - Ensure the structure flows logically and covers all key aspects of the topic.
           - Incorporate related keywords naturally into the headings where appropriate.

        3. Key Points to Address (in English)
           - List 5-7 crucial points that the content must cover to be competitive.
           - Base these points on gaps identified in the SERP analysis and high-value information from top competitors.
           - Ensure these points are reflected in the Content Structure, either as headings or as bullet points under relevant headings.
           - Present each point as a clear, actionable statement.

        4. Unique Angles (in English)
           - Suggest 3-5 unique perspectives or approaches not currently covered by top competitors or the Reference URL (if provided).
           - These should provide added value and help the content stand out in search results.
           - Ensure these unique angles are incorporated into the Content Structure, either as new headings or as points under existing headings.
           - Briefly explain how each angle contributes to the content's competitiveness.

        5. Related Keywords (in {target_language})
           - List 10-15 highly relevant keywords or phrases from the provided data, translated to {target_language}.
           - Organize them by relevance or importance to the main topic.
           - Indicate how these keywords should be incorporated into the Content Structure.

        6. Content Specifications (in English)
           - Recommended word count: Provide a range based on top-performing content in the SERP.
           - Suggested number of images or visual elements.
           - Specify any other content types (e.g., videos, infographics) that would enhance the piece.

        7. Related links (in English)
           - Use ONLY the links provided in the 'Potential Outlinks' section.
           - For each outlink, provide:
             a) The full URL
             b) A suggested anchor text (in {target_language}) based on the context of the brief's content and outline
             c) A brief explanation of its relevance (1-2 sentences)
           - If no potential outlinks are provided, state that no outlink strategy is available for this brief.

        Ensure the brief is actionable, specific, and tailored to the target keyword and audience. Use only the provided input data without adding extra information or explanations.

        Output Format:
        Present the SEO Content Brief in a clear, structured format using Markdown syntax for headings and lists. Use the following structure:

        # SEO Content Brief: [keyword in {target_language}]

        ## SERP Analysis

        ## Content Structure
        [This section MUST contain a single, coherent, detailed, hierarchical outline with proper H1, H2, H3, and H4 tags, incorporating all provided data sources and fully translated into {target_language}]

        ## Key Points to Address

        ## Unique Angles

        ## Related Keywords

        ## Content Specifications

        ## Related links

        Remember, only the Content Structure, target keyword, and Related Keywords sections should be in {target_language}. All other sections should be in English.
        """

        return prompt

    def _format_links(self, links):
        if not links:
            return "No potential link sources available."
        formatted_links = []
        for link in links:
            formatted_links.append(f"- {link['url']} (H1: {link['h1']}, Similarity: {link['similarity']:.2f}, Cluster: {link['cluster']})")
        return "\n".join(formatted_links)