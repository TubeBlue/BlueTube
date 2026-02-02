"""
Blue Tube - AnalDin.com Scraper
Scrapes video content from analdin.com
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin
import time


class AnalDinScraper:
    """Scraper for analdin.com website"""
    
    def __init__(self):
        self.base_url = "https://www.analdin.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_homepage(self, max_videos: int = 500) -> List[Dict]:
        """Scrape videos from multiple pages"""
        print(f"Scraping AnalDin.com for up to {max_videos} videos...")
        
        videos = []
        page = 1
        
        try:
            while len(videos) < max_videos:
                url = f"{self.base_url}/?page={page}" if page > 1 else self.base_url
                
                print(f"Page {page}: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find video containers
                video_elements = soup.find_all('div', class_='thumb-block')
                if not video_elements:
                    video_elements = soup.find_all('div', class_='item')
                
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
                            video_data['id'] = f"analdin_{len(videos) + 1}"
                            video_data['source'] = 'analdin.com'
                            videos.append(video_data)
                            page_videos += 1
                    except Exception as e:
                        continue
                
                print(f"✓ Scraped {page_videos} videos from page {page} (Total: {len(videos)})")
                
                if page_videos == 0 or len(videos) >= max_videos:
                    break
                
                page += 1
                time.sleep(0.3)
            
            print(f"\n✅ AnalDin: Scraped {len(videos)} videos from {page} pages")
            return videos
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return videos
    
    def _extract_video_data(self, element) -> Optional[Dict]:
        """Extract video data from element"""
        video_data = {}
        
        # Get video link and title
        link = element.find('a', class_='thumb') or element.find('a')
        if link:
            video_url = link.get('href', '')
            if video_url and not video_url.startswith('http'):
                video_url = urljoin(self.base_url, video_url)
            video_data['video_url'] = video_url
            
            # Extract video ID from URL - pattern: /videos/{id}/
            match = re.search(r'/videos?/(\d+)', video_url)
            if match:
                video_id = match.group(1)
                video_data['video_id'] = video_id
                video_data['embed_url'] = f"https://www.analdin.com/embed/{video_id}"
            
            # Get title
            title = link.get('title', '')
            if title:
                video_data['title'] = title
        
        # Try alternative title location
        if not video_data.get('title'):
            title_elem = element.find('div', class_='thumb-title') or element.find('h3')
            if title_elem:
                video_data['title'] = title_elem.get_text(strip=True)
        
        # Get thumbnail
        img = element.find('img')
        if img:
            thumbnail = img.get('data-src') or img.get('src')
            if thumbnail and not thumbnail.startswith('http'):
                thumbnail = urljoin(self.base_url, thumbnail)
            video_data['thumbnail'] = thumbnail
        
        # Get duration
        duration_elem = element.find('div', class_='duration') or element.find('span', class_='duration')
        if duration_elem:
            video_data['duration'] = duration_elem.get_text(strip=True)
        
        return video_data if video_data.get('title') else None


def main():
    """Test the scraper"""
    scraper = AnalDinScraper()
    videos = scraper.scrape_homepage(max_videos=300)
    
    if videos:
        print(f"\n✅ Total: {len(videos)} videos from AnalDin.com")
        with open('analdin_videos.json', 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)
        print("Saved to analdin_videos.json")


if __name__ == "__main__":
    main()
