import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os
import re

# List of URLs to crawl
urls = [
    "https://brunch.co.kr/@andkakao/317",
    "https://brunch.co.kr/@andkakao/321",
    "https://brunch.co.kr/@andkakao/322",
    "https://brunch.co.kr/@andkakao/324",
    "https://brunch.co.kr/@andkakao/323",
    "https://brunch.co.kr/@andkakao/325",
    "https://brunch.co.kr/@andkakao/326",
    "https://brunch.co.kr/@andkakao/327"
]

# Ensure output directory exists
output_dir = "question"
os.makedirs(output_dir, exist_ok=True)

def clean_filename(title):
    # Remove invalid characters for filenames
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

def crawl_url(url, index):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('h1', class_='cover_title') or soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else f"Question_{index}"
        
        # Extract content
        # Brunch articles usually have content in a div with class 'wrap_body' or similar. 
        # Sometimes it's just in the body, but we want to avoid nav/footer.
        # Let's try to find the main content container.
        content_div = soup.find('div', class_='wrap_body')
        
        if not content_div:
            # Fallback if specific class not found, though wrap_body is standard for Brunch
            print(f"Warning: 'wrap_body' not found for {url}. Using body tag.")
            content_div = soup.body

        # Convert to Markdown
        # We can exclude some tags if needed, but default is usually okay.
        markdown_content = md(str(content_div), heading_style="ATX")
        
        # Clean up excessive newlines
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # Save to file
        filename = f"{index}_{clean_filename(title)}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"Source: {url}\n\n")
            f.write(markdown_content)
            
        print(f"Successfully saved: {filepath}")
        
    except Exception as e:
        print(f"Error processing {url}: {e}")

def main():
    print("Starting crawl...")
    for i, url in enumerate(urls, 1):
        crawl_url(url, i)
    print("Crawling finished.")

if __name__ == "__main__":
    main()
