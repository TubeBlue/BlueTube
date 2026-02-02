"""
Test scraper to see what HTML structure websites use
"""

import requests
from bs4 import BeautifulSoup

def test_site(url, name):
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*70}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find video containers
        selectors_to_try = [
            ('div', 'thumb-block'),
            ('div', 'box'),
            ('div', 'item'),
            ('div', 'video'),
            ('article', None),
            ('div', 'video-item'),
            ('div', 'th'),
        ]
        
        for tag, class_name in selectors_to_try:
            if class_name:
                elements = soup.find_all(tag, class_=class_name)
            else:
                elements = soup.find_all(tag)
            
            if elements:
                print(f"\n✅ Found {len(elements)} elements with: <{tag} class='{class_name}'>")
                
                # Show first element structure
                if elements:
                    first = elements[0]
                    print(f"\nFirst element structure:")
                    print(f"  Has <a>: {bool(first.find('a'))}")
                    if first.find('a'):
                        link = first.find('a')
                        print(f"  Link href: {link.get('href', 'None')[:60]}")
                        print(f"  Link title: {link.get('title', 'None')[:60]}")
                    print(f"  Has <img>: {bool(first.find('img'))}")
                    if first.find('img'):
                        img = first.find('img')
                        print(f"  Img src: {img.get('src', 'None')[:60]}")
                        print(f"  Img data-src: {img.get('data-src', 'None')[:60]}")
                break
        else:
            print("\n❌ No video containers found with common selectors")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

# Test all sites
sites = [
    ('https://upornia.com', 'Upornia'),
    ('https://www.drtuber.com', 'DrTuber'),
    ('https://txxx.com', 'Txxx'),
]

for url, name in sites:
    test_site(url, name)

print(f"\n{'='*70}")
print("Testing complete!")
print(f"{'='*70}")
