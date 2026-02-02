"""
Blue Tube - XVideos Scraper
Scrapes video content from xvideos.com
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin


class XVideosScraper:
    """Scraper for xvideos.com website"""
    
    def __init__(self):
        self.base_url = "https://www.xvideos.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_homepage(self, max_videos: int = 24) -> List[Dict]:
        """
        Scrape videos from the homepage
        
        Args:
            max_videos: Maximum number of videos to scrape
            
        Returns:
            List of video dictionaries containing title, duration, embed_url, etc.
        """
        print(f"Scraping XVideos homepage for up to {max_videos} videos...")
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            videos = []
            
            # Find video containers - XVideos uses div with class 'thumb-block'
            video_elements = soup.find_all('div', class_='thumb-block')
            
            if not video_elements:
                print("No video elements found with class 'thumb-block', trying alternative...")
                video_elements = soup.find_all('div', class_='thumb')
            
            print(f"Found {len(video_elements)} video elements")
            
            for idx, element in enumerate(video_elements[:max_videos]):
                try:
                    video_data = self._extract_video_data(element)
                    if video_data:
                        video_data['id'] = f"xvideos_{idx + 1}"
                        video_data['source'] = 'xvideos'
                        videos.append(video_data)
                        print(f"Scraped video {idx + 1}: {video_data.get('title', 'Unknown')[:50]}")
                except Exception as e:
                    print(f"Error extracting video {idx + 1}: {str(e)}")
                    continue
            
            print(f"Successfully scraped {len(videos)} videos from XVideos")
            return videos
            
        except requests.RequestException as e:
            print(f"Error fetching XVideos homepage: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error in scrape_homepage: {str(e)}")
            return []
    
    def _extract_video_data(self, element) -> Optional[Dict]:
        """Extract video data from a video element"""
        
        video_data = {}
        
        # Find the main video link - look for any link with /video in href
        all_links = element.find_all('a')
        video_link = None
        
        for link in all_links:
            href = link.get('href', '')
            if '/video' in href:
                video_link = link
                break
        
        if not video_link:
            return None
        
        # Get title from title attribute
        title = video_link.get('title', '').strip()
        
        if not title:
            # Fallback: try to find title in p tag
            title_elem = element.find('p', class_='title')
            if title_elem:
                title = title_elem.get_text(strip=True)
        
        if not title:
            return None
        
        # Clean up title
        title = ' '.join(title.split())
        video_data['title'] = title
        
        # Get video URL
        video_url = video_link.get('href', '')
        if video_url and not video_url.startswith('http'):
            video_url = urljoin(self.base_url, video_url)
        video_data['video_url'] = video_url
        
        # Extract thumbnail
        img_elem = element.find('img')
        if img_elem:
            thumbnail = img_elem.get('data-src') or img_elem.get('src') or img_elem.get('data-thumb_url')
            if thumbnail:
                if not thumbnail.startswith('http'):
                    thumbnail = urljoin(self.base_url, thumbnail)
                video_data['thumbnail'] = thumbnail
        
        # Extract duration - look for span with bg class
        duration_elem = element.find('span', class_='bg')
        if not duration_elem:
            duration_elem = element.find('span', class_='duration')
        if duration_elem:
            video_data['duration'] = duration_elem.get_text(strip=True)
        
        # Extract video ID from data-eid attribute (more reliable)
        video_id = element.get('data-eid')
        if video_id:
            video_data['video_id'] = video_id
            video_data['embed_url'] = f"{self.base_url}/embedframe/{video_id}"
        elif video_data.get('video_url'):
            video_data['video_id'] = self._extract_video_id(video_data['video_url'])
            video_data['embed_url'] = self._generate_embed_url(video_data['video_url'])
        
        return video_data
    
    def _extract_video_id(self, video_url: str) -> str:
        """
        Extract video ID from URL
        Example: https://www.xvideos.com/video12345/title -> 12345
        Example: https://www.xvideos.com/video.udhhopoa0f8 -> udhhopoa0f8
        """
        # Try pattern: /video12345/title or /video.abc123
        match = re.search(r'/video\.?([^/]+)', video_url)
        if match:
            video_id = match.group(1)
            # Remove any trailing part after slash
            if '/' in video_id:
                video_id = video_id.split('/')[0]
            return video_id
        
        return ''
    
    def _generate_embed_url(self, video_url: str) -> str:
        """
        Generate embed URL from video page URL
        Example: https://www.xvideos.com/video12345/title
        Becomes: https://www.xvideos.com/embedframe/12345
        """
        video_id = self._extract_video_id(video_url)
        if video_id:
            return f"{self.base_url}/embedframe/{video_id}"
        
        # Fallback to video URL
        return video_url


def main():
    """Test the scraper"""
    scraper = XVideosScraper()
    
    # Test scraping homepage
    print("\n" + "="*50)
    print("Testing XVideos Homepage Scraper")
    print("="*50)
    videos = scraper.scrape_homepage(max_videos=5)
    
    if videos:
        print(f"\nSuccessfully scraped {len(videos)} videos!")
        print("\nSample video:")
        import json
        print(json.dumps(videos[0], indent=2))
    else:
        print("\nNo videos scraped. Please check the website structure.")


if __name__ == "__main__":
    main()
