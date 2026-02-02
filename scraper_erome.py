"""
Blue Tube - Erome Scraper
Scrapes video content from erome.com/explore
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin


class EromeScraper:
    """Scraper for erome.com website"""
    
    def __init__(self):
        self.base_url = "https://www.erome.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_homepage(self, max_videos: int = 10) -> List[Dict]:
        """Scrape videos from the explore page"""
        print(f"Scraping Erome explore page for up to {max_videos} videos...")
        
        try:
            url = f"{self.base_url}/explore"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            videos = []
            
            # Find album/video containers
            video_elements = soup.find_all('div', class_='album')
            
            if not video_elements:
                video_elements = soup.find_all('div', class_='item')
            
            if not video_elements:
                video_elements = soup.find_all('article')
            
            print(f"Found {len(video_elements)} video elements")
            
            for idx, element in enumerate(video_elements[:max_videos]):
                try:
                    video_data = self._extract_video_data(element)
                    if video_data:
                        video_data['id'] = f"erome_{idx + 1}"
                        video_data['source'] = 'erome'
                        videos.append(video_data)
                        print(f"Scraped Erome video {idx + 1}: {video_data.get('title', 'Unknown')[:50]}")
                except Exception as e:
                    print(f"Error extracting Erome video {idx + 1}: {str(e)}")
                    continue
            
            print(f"Successfully scraped {len(videos)} videos from Erome")
            return videos
            
        except Exception as e:
            print(f"Error scraping Erome: {str(e)}")
            return []
    
    def _extract_video_data(self, element) -> Optional[Dict]:
        """Extract video data from a video element"""
        
        video_data = {}
        
        # Find video link
        video_link = element.find('a', href=re.compile(r'/a/'))
        
        if not video_link:
            video_link = element.find('a')
        
        if not video_link:
            return None
        
        # Get title
        title = video_link.get('title', '').strip()
        if not title:
            title_elem = element.find('h3') or element.find('h2')
            if title_elem:
                title = title_elem.get_text(strip=True)
        
        if not title:
            # Use URL as fallback title
            href = video_link.get('href', '')
            title = href.split('/')[-1].replace('-', ' ').title() if href else 'Video'
        
        video_data['title'] = ' '.join(title.split())
        
        # Get video URL
        video_url = video_link.get('href', '')
        if video_url and not video_url.startswith('http'):
            video_url = urljoin(self.base_url, video_url)
        video_data['video_url'] = video_url
        video_data['embed_url'] = video_url  # Erome doesn't have standard embed, use page URL
        
        # Extract thumbnail
        img_elem = element.find('img')
        if img_elem:
            thumbnail = img_elem.get('data-src') or img_elem.get('src')
            if thumbnail and not thumbnail.startswith('http'):
                thumbnail = urljoin(self.base_url, thumbnail)
            video_data['thumbnail'] = thumbnail
        
        # Extract duration if available
        duration_elem = element.find('span', class_='duration')
        if duration_elem:
            video_data['duration'] = duration_elem.get_text(strip=True)
        
        return video_data


def main():
    """Test the scraper"""
    scraper = EromeScraper()
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
