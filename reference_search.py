import os
import requests
from urllib.parse import urlparse
import streamlit as st
from typing import List, Dict
from dotenv import load_dotenv


load_dotenv()  # Make sure this is called before accessing the variables

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def get_domain_credibility(url: str) -> bool:
    """Check if the domain is from a credible educational source"""
    credible_domains = [
        '.edu', '.gov', 'wikipedia.org', 'khanacademy.org',
        'britannica.com', 'nationalgeographic.com', 'nasa.gov',
        'sciencemag.org', 'ted.com', 'mit.edu', 'harvard.edu',
        'oup.com', 'springer.com', 'nature.com', 'science.org'
    ]
    domain = urlparse(url).netloc.lower()
    return any(credible in domain for credible in credible_domains)

def google_custom_search(query: str, num_results: int = 5) -> List[Dict]:
    """Perform a search using Google Custom Search JSON API"""
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&num={num_results}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        results = []
        if 'items' in data:
            for item in data['items']:
                results.append({
                    'url': item['link'],
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'domain': urlparse(item['link']).netloc.replace('www.', '')
                })
        return results
        
    except Exception as e:
        st.error(f"Error performing Google search: {str(e)}")
        return []

def search_references(topic: str, subject: str, grade_level: str, num_results: int = 5) -> List[Dict]:
    """Search for credible reference links related to the topic"""
    query = f"{topic} {subject} {grade_level} educational resources"
    
    search_results = google_custom_search(query, num_results)
    
    credible_results = []
    for result in search_results:
        if get_domain_credibility(result['url']):
            credible_results.append(result)
            if len(credible_results) >= 3:  # Limit to 3 results
                break
    
    return credible_results

def render_references(references: List[Dict]) -> str:
    """Display references as simple links at the end"""
    if not references:
        return ""
    
    # Remove duplicate references
    unique_refs = []
    seen_urls = set()
    for ref in references:
        if ref['url'] not in seen_urls:
            unique_refs.append(ref)
            seen_urls.add(ref['url'])
    
    # Simple markdown format
    markdown = "### 📚 Recommended References\n"
    for ref in unique_refs[:10]:  # Limit to 10 references max
        markdown += f"- [{ref['domain']}]({ref['url']}) - {ref.get('snippet', '')[:100]}...\n"
    
    return markdown