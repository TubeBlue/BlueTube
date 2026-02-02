"""Debug XVideos scraping"""
import requests
from bs4 import BeautifulSoup
import re

url = "https://www.xvideos.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("Fetching XVideos homepage...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

print("\nFinding video elements...")
video_divs = soup.find_all('div', class_='thumb-block')
print(f"Found {len(video_divs)} divs with class 'thumb-block'")

if len(video_divs) > 0:
    print("\n=== First Video Element ===")
    first = video_divs[0]
    print(first.prettify()[:2000])
    
    # Find all links
    links = first.find_all('a')
    print(f"\n\nFound {len(links)} links")
    for i, link in enumerate(links):
        href = link.get('href', '')
        if '/video' in href:
            print(f"\nVideo Link {i+1}:")
            print(f"  href: {href}")
            print(f"  title: {link.get('title')}")
            print(f"  text: {link.get_text(strip=True)[:100]}")
