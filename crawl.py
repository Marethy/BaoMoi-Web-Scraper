import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def crawl_page(page_id):
    url = f"https://baomoi.com/trang{page_id}.epi"  # Replace with the actual URL

    print(f"Crawling {url}...")
    
    # Make an HTTP request to fetch the page content
    response = requests.get(url)
    
    if response.status_code == 200:
        page_content = response.content
        
        # Initialize BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Find all divs with the specific class
        cards = soup.find_all('div', class_='bm-card')

        # List to store the extracted information from the page
        page_data = []
        
        # Iterate through each card and extract the desired information
        for card in cards:
            # Extract title and URL
            title_tag = card.find('h3').find('a', title=True)
            title = title_tag['title'] if title_tag else 'No Title'
            article_url = title_tag['href'] if title_tag else 'No URL'

            # Extract image source (from picture > source or img tag)
            img_tag = card.find('figure').find('picture').find('source')
            img_src = img_tag['srcset'] if img_tag and 'srcset' in img_tag.attrs else 'No Image'

            # Extract time
            time_tag = card.find('time')
            time = time_tag['datetime'] if time_tag else 'No Time'

            # Append the extracted information to the list
            if 'http' in img_src:
                page_data.append({
                'Title': title,
                'URL': 'https://baomoi.com'+ article_url,
                'Image': img_src,
                'Time': time
            
            })

        return page_data
    
    else:
        print(f"Failed to fetch the URL: {url}. Status code: {response.status_code}")
        return []
# Main function to crawl multiple pages
def crawl_multiple_pages(start_page, end_page):
    all_data = []

    for page_id in range(start_page, end_page + 1):
        # Crawl the current page and collect its data
        page_data = crawl_page(page_id)
        all_data.extend(page_data)
        
        # Sleep for a short while to avoid overwhelming the server

    return all_data

# Crawl pages from 1 to 15
crawled_data = crawl_multiple_pages(1, 50)

# Create a DataFrame from the list
df = pd.DataFrame(crawled_data)

# Export the DataFrame to an Excel file
df.to_excel('crawled_data.xlsx', index=False)

print("Data has been exported to 'crawled_data.xlsx'")