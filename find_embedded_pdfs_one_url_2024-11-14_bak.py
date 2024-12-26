import requests
from bs4 import BeautifulSoup
import re

def find_embedded_pdfs(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_links = set()

    # Find all <a> tags with href attributes containing 'pdf'
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf') or 'pdf' in href.lower():
            pdf_url = requests.compat.urljoin(url, href)
            pdf_links.add(pdf_url)

    # Find embedded PDF links in inline JavaScript code (e.g., adobe_dc_view_sdk)
    for script in soup.find_all('script'):
        if script.string:
            # Search for URLs in the form "url": "/path/to/file.pdf"
            pdf_matches = re.findall(r'url:\s*["\'](/[^"\']+\.pdf)["\']', script.string)
            for match in pdf_matches:
                pdf_url = requests.compat.urljoin(url, match)
                pdf_links.add(pdf_url)

    # Display results
    if pdf_links:
        print("Found the following PDF links:")
        for pdf in pdf_links:
            print(pdf)
    else:
        print("No PDFs found on this page.")

    return list(pdf_links)

# URL of the directive page to test
url = "https://www.usda.gov/directives/dr-3300-015"
pdf_links = find_embedded_pdfs(url)
