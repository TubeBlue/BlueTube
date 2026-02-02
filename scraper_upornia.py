"""
Blue Tube - Upornia.com Scraper
Scrapes video content from upornia.com
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin
import time


class UporniaScraper:
    """Scraper for upornia.com website"""
    
    def __init__(self):
        self.base_url = "https://upornia.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_homepage(self, max_videos: int = 500) -> List[Dict]:
        """Scrape videos from multiple pages"""
        print(f"Scraping Upornia.com for up to {max_videos} videos...")
        
        videos = []
        page = 1
        
        try:
            while len(videos) < max_videos:
                url = f"{self.base_url}/?page={page}" if page > 1 else self.base_url
                
                print(f"Page {page}: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find video containers - try multiple selectors
                video_elements = soup.find_all('div', class_='box')
                if not video_elements:
                    video_elements = soup.find_all('div', class_='item')
                if not video_elements:
                    video_elements = soup.find_all('article')
                
                if not video_elements:
                    print(f"No videos found on page {page}. Stopping.")
                    break
                
                print(f"Found {len(video_elements)} videos on page {page}")
                
                page_videos = 0
                for element in video_elements:
                    if len(videos) >= max_videos:
                        break
                        
                    try:
                        video_data = self._extract_video_data(element)
                        if video_data:
                            video_data['id'] = f"upornia_{len(videos) + 1}"
                            video_data['source'] = 'upornia.com'
                            videos.append(video_data)
                            page_videos += 1
                    except Exception as e:
                        continue
                
                print(f"✓ Scraped {page_videos} videos from page {page} (Total: {len(videos)})")
                
                if page_videos == 0 or len(videos) >= max_videos:
                    break
                
                page += 1
                time.sleep(0.3)
            
            print(f"\n✅ Upornia: Scraped {len(videos)} videos from {page} pages")
            return videos
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return videos
    
    def _extract_video_data(self, element) -> Optional[Dict]:
        """Extract video data from element"""
        video_data = {}
        
        # Find all links - try multiple approaches
        link = element.find('a', class_='link') or element.find('a', href=re.compile(r'/videos?/'))
        if not link:
            # Try any link
            links = element.find_all('a')
            for l in links:
                href = l.get('href', '')
                if '/video' in href:
                    link = l
                    break
        
        if link:
            video_url = link.get('href', '')
            if video_url and not video_url.startswith('http'):
                video_url = urljoin(self.base_url, video_url)
            video_data['video_url'] = video_url
            
            # Extract video ID - try multiple patterns
            match = re.search(r'/videos?/(\d+)', video_url)
            if not match:
                match = re.search(r'/(\d+)/', video_url)
            if match:
                video_id = match.group(1)
                video_data['video_id'] = video_id
                video_data['embed_url'] = f"https://upornia.com/embed/{video_id}"
            
            # Get title - try multiple sources
            title = link.get('title', '') or link.get('alt', '')
            if not title:
                # Try text content
                title = link.get_text(strip=True)
                if len(title) > 100:  # Too long, probably not a title
                    title = ''
            if not title:
                # Try within element
                title_elem = element.find('div', class_='title') or element.find('h3') or element.find('h2') or element.find('span', class_='title')
                if title_elem:
                    title = title_elem.get_text(strip=True)
            if title:
                video_data['title'] = title.strip()
        
        # Get thumbnail - try all possible attributes
        img = element.find('img')
        if img:
            thumbnail = img.get('data-src') or img.get('data-original') or img.get('data-lazy') or img.get('src')
            if thumbnail:
                if thumbnail.startswith('//'):
                    thumbnail = 'https:' + thumbnail
                elif not thumbnail.startswith('http'):
                    thumbnail = urljoin(self.base_url, thumbnail)
                video_data['thumbnail'] = thumbnail
        
        # Get duration
        duration_elem = element.find('div', class_='duration') or element.find('span', class_='time') or element.find('span', class_='duration')
        if duration_elem:
            video_data['duration'] = duration_elem.get_text(strip=True)
        
        return video_data if video_data.get('title') and video_data.get('video_id') else None


def main():
    """Test the scraper"""
    scraper = UporniaScraper()
    videos = scraper.scrape_homepage(max_videos=300)
    
    if videos:
        print(f"\n✅ Total: {len(videos)} videos from Upornia.com")
        with open('upornia_videos.json', 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)
        print("Saved to upornia_videos.json")


if __name__ == "__main__":
    main()
