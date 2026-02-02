"""
Blue Tube - Video Scraper
Scrapes video content from eporner.com
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin
import time


class EpornerScraper:
    """Scraper for eporner.com website"""
    
    def __init__(self):
        self.base_url = "https://www.eporner.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_homepage(self, max_videos: int = 100) -> List[Dict]:
        """
        Scrape videos from homepage and multiple pages
        
        Args:
            max_videos: Maximum number of videos to scrape
            
        Returns:
            List of video dictionaries containing title, duration, embed_url, etc.
        """
        print(f"Scraping for up to {max_videos} videos...")
        
        videos = []
        page = 1
        videos_per_page = 60  # Approximate
        
        try:
            while len(videos) < max_videos:
                # Construct URL for current page
                if page == 1:
                    url = self.base_url
                else:
                    url = f"{self.base_url}/{page}/"
                
                print(f"\nPage {page}: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find video containers
                video_elements = soup.find_all('div', class_='mb')
                
                if not video_elements:
                    print("No video elements found with class 'mb', trying alternative selectors...")
                    video_elements = soup.find_all('div', class_='thumbname')
                
                if not video_elements:
                    print(f"No videos found on page {page}. Stopping.")
                    break
                
                print(f"Found {len(video_elements)} video elements on page {page}")
                
                page_videos = 0
                for element in video_elements:
                    if len(videos) >= max_videos:
                        break
                        
                    try:
                        video_data = self._extract_video_data(element)
                        if video_data:
                            video_data['id'] = f"video_{len(videos) + 1}"
                            videos.append(video_data)
                            page_videos += 1
                    except Exception as e:
                        print(f"Error extracting video: {str(e)}")
                        continue
                
                print(f"✓ Scraped {page_videos} videos from page {page} (Total: {len(videos)})")
                
                # Check if we should continue
                if page_videos == 0 or len(videos) >= max_videos:
                    break
                
                page += 1
                time.sleep(0.3)  # Small delay between pages
            
            print(f"\n✅ Successfully scraped {len(videos)} videos from {page} pages")
            return videos
            
        except requests.RequestException as e:
            print(f"Error fetching page: {str(e)}")
            return videos
        except Exception as e:
            print(f"Unexpected error in scrape_homepage: {str(e)}")
            return videos
    
    def _extract_video_data(self, element) -> Optional[Dict]:
        """Extract video data from a video element"""
        
        video_data = {}
        
        # Extract title from <p class="mbtit"> which contains the title link
        title_elem = element.find('p', class_='mbtit')
        if title_elem:
            title_link = title_elem.find('a')
            if title_link:
                title = title_link.get_text(strip=True)
                video_url = title_link.get('href', '')
                
                # Clean up title
                title = ' '.join(title.split())
                video_data['title'] = title
                
                # Get video URL
                if video_url and not video_url.startswith('http'):
                    video_url = urljoin(self.base_url, video_url)
                video_data['video_url'] = video_url
        
        # Fallback: find any link with /video- in href
        if not video_data.get('title'):
            all_links = element.find_all('a')
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if '/video-' in href and text and text != 'Uploader':
                    video_data['title'] = ' '.join(text.split())
                    video_url = href
                    if not video_url.startswith('http'):
                        video_url = urljoin(self.base_url, video_url)
                    video_data['video_url'] = video_url
                    break
        
        if not video_data.get('title'):
            return None
        
        # Extract thumbnail
        img_elem = element.find('img')
        if img_elem:
            thumbnail = img_elem.get('data-src') or img_elem.get('src') or img_elem.get('data-original')
            if thumbnail and not thumbnail.startswith('http'):
                thumbnail = urljoin(self.base_url, thumbnail)
            video_data['thumbnail'] = thumbnail
        
        # Extract duration
        duration_elem = element.find('div', class_='mbtim')
        if not duration_elem:
            duration_elem = element.find('span', class_='duration')
        if not duration_elem:
            duration_elem = element.find('div', class_='duration')
        if not duration_elem:
            # Try to find any element with time format
            time_text = element.find(string=re.compile(r'\d+:\d+'))
            if time_text:
                video_data['duration'] = time_text.strip()
        else:
            video_data['duration'] = duration_elem.text.strip()
        
        # Extract views
        views_elem = element.find('div', class_='mbvie')
        if not views_elem:
            views_elem = element.find('span', class_='views')
        if not views_elem:
            views_elem = element.find(string=re.compile(r'\d+[KM]?\s*views?', re.IGNORECASE))
        if views_elem:
            video_data['views'] = views_elem.text.strip() if hasattr(views_elem, 'text') else str(views_elem).strip()
        
        # Generate proper embed URL from video URL
        if video_data.get('video_url'):
            video_data['video_id'] = self._extract_video_id(video_data['video_url'])
            video_data['embed_url'] = self._generate_embed_url(video_data['video_url'])
        
        return video_data if video_data.get('title') else None
    
    def _extract_video_id(self, video_url: str) -> str:
        """
        Extract video ID from URL
        Example: https://www.eporner.com/video-xUTa1uKePgw/title -> xUTa1uKePgw
        """
        # Try pattern: /video-ID/title
        match = re.search(r'/video-([^/]+)/', video_url)
        if match:
            return match.group(1)
        
        # Try pattern: /hd-porn/ID/title
        match = re.search(r'/hd-porn/([^/]+)/', video_url)
        if match:
            return match.group(1)
        
        # Try pattern with just ID
        match = re.search(r'/([a-zA-Z0-9_-]{8,})/', video_url)
        if match:
            return match.group(1)
        
        return ''
    
    def _generate_embed_url(self, video_url: str) -> str:
        """
        Generate proper embed URL from video page URL
        Example: https://www.eporner.com/video-xUTa1uKePgw/title
        Becomes: https://www.eporner.com/embed/xUTa1uKePgw/
        """
        video_id = self._extract_video_id(video_url)
        if video_id:
            return f"{self.base_url}/embed/{video_id}/"
        
        # Fallback to video URL
        return video_url
    
    def scrape_video_details(self, video_url: str) -> Optional[Dict]:
        """
        Scrape detailed information from a video page
        
        Args:
            video_url: URL of the video page
            
        Returns:
            Dictionary with detailed video information
        """
        try:
            print(f"Scraping video details from: {video_url}")
            response = self.session.get(video_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            details = {}
            
            # Title - Try multiple selectors
            title_elem = soup.find('h1')
            if not title_elem:
                title_elem = soup.find('h1', class_='title')
            if not title_elem:
                title_elem = soup.find('div', class_='video-title')
            if title_elem:
                details['title'] = title_elem.text.strip()
            
            # Description - Try multiple selectors
            desc_elem = soup.find('div', class_='video-description')
            if not desc_elem:
                desc_elem = soup.find('div', class_='description')
            if not desc_elem:
                desc_elem = soup.find('div', id='video-description')
            if not desc_elem:
                desc_elem = soup.find('p', class_='description')
            if not desc_elem:
                # Try meta description
                meta_desc = soup.find('meta', {'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    details['description'] = meta_desc['content'].strip()
            else:
                details['description'] = desc_elem.text.strip()
            
            # Views - Try multiple selectors and patterns
            views_elem = soup.find('span', class_='views-count')
            if not views_elem:
                views_elem = soup.find('div', class_='views')
            if not views_elem:
                views_elem = soup.find('span', class_='view-count')
            if not views_elem:
                views_elem = soup.find(string=re.compile(r'(\d+[\d,\.]*[KMB]?)\s*views?', re.IGNORECASE))
            if views_elem:
                if hasattr(views_elem, 'text'):
                    views_text = views_elem.text.strip()
                else:
                    views_text = str(views_elem).strip()
                # Extract just the number part
                match = re.search(r'(\d+[\d,\.]*[KMB]?)\s*views?', views_text, re.IGNORECASE)
                if match:
                    details['views'] = match.group(1)
                else:
                    details['views'] = views_text
            
            # Duration - Try multiple selectors
            duration_elem = soup.find('span', class_='duration')
            if not duration_elem:
                duration_elem = soup.find('div', class_='duration')
            if not duration_elem:
                duration_elem = soup.find('time')
            if duration_elem:
                details['duration'] = duration_elem.text.strip()
            
            # Embed URL
            details['embed_url'] = self._generate_embed_url(video_url)
            
            return details
            
        except Exception as e:
            print(f"Error scraping video details: {str(e)}")
            return None
    
    def search_videos(self, query: str, max_videos: int = 20) -> List[Dict]:
        """
        Search for videos with a query
        
        Args:
            query: Search query
            max_videos: Maximum number of videos to return
            
        Returns:
            List of video dictionaries
        """
        try:
            search_url = f"{self.base_url}/search/{query}/"
            print(f"Searching for: {query}")
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            videos = []
            
            video_elements = soup.find_all('div', class_='mb')[:max_videos]
            
            for idx, element in enumerate(video_elements):
                try:
                    video_data = self._extract_video_data(element)
                    if video_data:
                        video_data['id'] = f"search_{idx + 1}"
                        videos.append(video_data)
                except Exception as e:
                    print(f"Error extracting search result {idx + 1}: {str(e)}")
                    continue
            
            print(f"Found {len(videos)} videos for query: {query}")
            return videos
            
        except Exception as e:
            print(f"Error searching videos: {str(e)}")
            return []


def main():
    """Test the scraper"""
    scraper = EpornerScraper()
    
    # Test scraping homepage
    print("\n" + "="*70)
    print("🚀 MASSIVE SCRAPE: Fetching MAXIMUM Videos (1000+)")
    print("="*70)
    videos = scraper.scrape_homepage(max_videos=1500)
    
    if videos:
        print(f"\nSuccessfully scraped {len(videos)} videos!")
        print("\nSample video:")
        print(json.dumps(videos[0], indent=2))
    else:
        print("\nNo videos scraped. Please check the website structure.")
    
    # Save to file
    if videos:
        with open('scraped_videos.json', 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)
        print("\nVideos saved to scraped_videos.json")


if __name__ == "__main__":
    main()
