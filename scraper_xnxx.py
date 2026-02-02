"""
Blue Tube - XNXX Scraper
Scrapes video content from xnxx.com
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin


class XNXXScraper:
    """Scraper for xnxx.com website"""
    
    def __init__(self):
        self.base_url = "https://www.xnxx.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_homepage(self, max_videos: int = 20) -> List[Dict]:
        """Scrape videos from the homepage"""
        print(f"Scraping XNXX homepage for up to {max_videos} videos...")
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            videos = []
            
            # Find video containers
            video_elements = soup.find_all('div', class_='thumb-block')
            
            if not video_elements:
                video_elements = soup.find_all('div', class_='mozaique')
            
            print(f"Found {len(video_elements)} video elements")
            
            for idx, element in enumerate(video_elements[:max_videos]):
                try:
                    video_data = self._extract_video_data(element)
                    if video_data:
                        video_data['id'] = f"xnxx_{idx + 1}"
                        video_data['source'] = 'xnxx'
                        videos.append(video_data)
                        print(f"Scraped XNXX video {idx + 1}: {video_data.get('title', 'Unknown')[:50]}")
                except Exception as e:
                    print(f"Error extracting XNXX video {idx + 1}: {str(e)}")
                    continue
            
            print(f"Successfully scraped {len(videos)} videos from XNXX")
            return videos
            
        except Exception as e:
            print(f"Error scraping XNXX: {str(e)}")
            return []
    
    def _extract_video_data(self, element) -> Optional[Dict]:
        """Extract video data from a video element"""
        
        video_data = {}
        
        # Find video link
        video_link = element.find('a', href=re.compile(r'/video'))
        
        if not video_link:
            return None
        
        # Get title from title attribute or text
        title = video_link.get('title', '').strip()
        if not title:
            title_elem = video_link.find('p', class_='title')
            if title_elem:
                title = title_elem.get_text(strip=True)
        
        if not title:
            return None
        
        video_data['title'] = ' '.join(title.split())
        
        # Get video URL
        video_url = video_link.get('href', '')
        if video_url and not video_url.startswith('http'):
            video_url = urljoin(self.base_url, video_url)
        video_data['video_url'] = video_url
        
        # Extract thumbnail
        img_elem = element.find('img')
        if img_elem:
            thumbnail = img_elem.get('data-src') or img_elem.get('src')
            if thumbnail and not thumbnail.startswith('http'):
                thumbnail = urljoin(self.base_url, thumbnail)
            video_data['thumbnail'] = thumbnail
        
        # Extract duration
        duration_elem = element.find('p', class_='metadata')
        if duration_elem:
            duration_span = duration_elem.find('span', class_='duration')
            if duration_span:
                video_data['duration'] = duration_span.get_text(strip=True)
        
        # Extract video ID and generate embed URL
        video_id = self._extract_video_id(video_data.get('video_url', ''))
        if video_id:
            video_data['video_id'] = video_id
            video_data['embed_url'] = f"{self.base_url}/embedframe/{video_id}"
        
        return video_data
    
    def _extract_video_id(self, video_url: str) -> str:
        """
        Extract video ID from URL
        Example: https://www.xnxx.com/video-abc123/title -> abc123
        """
        match = re.search(r'/video-([^/]+)/', video_url)
        if match:
            return match.group(1)
        
        match = re.search(r'/video\.([^/]+)', video_url)
        if match:
            return match.group(1)
        
        return ''


def main():
    """Test the scraper"""
    scraper = XNXXScraper()
    videos = scraper.scrape_homepage(max_videos=3)
    
    if videos:
        print(f"\n✅ Successfully scraped {len(videos)} videos!")
        import json
        print("\nSample video:")
        print(json.dumps(videos[0], indent=2))
    else:
        print("\n❌ No videos scraped")


if __name__ == "__main__":
    main()
