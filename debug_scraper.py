"""Debug script to test scraping"""
import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://www.eporner.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("Fetching homepage...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

print("\nFinding video elements...")
video_divs = soup.find_all('div', class_='mb')
print(f"Found {len(video_divs)} divs with class 'mb'")

if len(video_divs) > 0:
    print("\n=== Testing First 3 Videos ===")
    for idx, video_div in enumerate(video_divs[:3]):
        print(f"\n--- Video {idx+1} ---")
        
        # Find all links
        all_links = video_div.find_all('a')
        video_link = None
        
        # Find the main video link
        for link in all_links:
            href = link.get('href', '')
            if '/video-' in href or '/hd-porn/' in href:
                video_link = link
                break
        
        # Try the new method
        title_elem = video_div.find('p', class_='mbtit')
        if title_elem:
            title_link = title_elem.find('a')
            if title_link:
                title = title_link.get_text(strip=True)
                title = ' '.join(title.split())
                video_url = title_link.get('href', '')
            
            print(f"Title: {title}")
            print(f"URL: {video_url}")
            
            # Extract video ID
            match = re.search(r'/video-([^/]+)/', video_url)
            if match:
                video_id = match.group(1)
                embed_url = f"https://www.eporner.com/embed/{video_id}/"
                print(f"Video ID: {video_id}")
                print(f"Embed URL: {embed_url}")
        else:
            print("No video link found!")
