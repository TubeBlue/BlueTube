"""Detailed debug for Eporner"""
import requests
from bs4 import BeautifulSoup

url = "https://www.eporner.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("Fetching Eporner homepage...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

print("\nFinding video elements...")
video_divs = soup.find_all('div', class_='mb')
print(f"Found {len(video_divs)} divs")

if len(video_divs) > 0:
    first = video_divs[0]
    print("\n=== First Video Full HTML ===")
    print(first.prettify()[:3000])
    
    print("\n\n=== Analyzing Links ===")
    links = first.find_all('a')
    for i, link in enumerate(links):
        print(f"\nLink {i+1}:")
        print(f"  Href: {link.get('href')}")
        print(f"  Title attr: {link.get('title')}")
        print(f"  Text: '{link.get_text(strip=True)}'")
        print(f"  Has /video-: {'/video-' in link.get('href', '')}")
