"""
Universal Browser-Based Scraper for JavaScript sites
Uses Selenium to handle dynamic content
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json
from typing import List, Dict, Optional


class UniversalBrowserScraper:
    """Universal scraper for JavaScript-rendered sites"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
    
    def init_driver(self):
        """Initialize Chrome WebDriver"""
        if self.driver:
            return
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Browser initialized")
    
    def close_driver(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_site(self, base_url, site_name, embed_pattern, max_videos=200):
        """
        Scrape videos from a site
        
        Args:
            base_url: Site homepage URL
            site_name: Name for identification
            embed_pattern: Pattern for embed URL (e.g., 'https://site.com/embed/{id}')
            max_videos: Maximum videos to scrape
        """
        print(f"\n🌐 Scraping {site_name}...")
        
        self.init_driver()
        videos = []
        page = 1
        
        try:
            while len(videos) < max_videos and page <= 5:  # Max 5 pages
                url = f"{base_url}?page={page}" if page > 1 else base_url
                print(f"  Page {page}: {url}")
                
                self.driver.get(url)
                time.sleep(3)  # Wait for JavaScript to load
                
                # Try to find video links with multiple selectors
                video_links = []
                selectors = [
                    '//a[contains(@href, "/video")]',
                    '//a[contains(@href, "/videos/")]',
                    '//div[contains(@class, "video")]//a',
                    '//div[contains(@class, "item")]//a',
                    '//div[contains(@class, "thumb")]//a',
                ]
                
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        if elements:
                            video_links = elements
                            break
                    except:
                        continue
                
                if not video_links:
                    print(f"  No videos found on page {page}")
                    break
                
                print(f"  Found {len(video_links)} potential videos")
                
                # Extract video data
                page_videos = 0
                for link in video_links:
                    if len(videos) >= max_videos:
                        break
                    
                    try:
                        video_url = link.get_attribute('href')
                        if not video_url or '/video' not in video_url:
                            continue
                        
                        # Extract video ID
                        match = re.search(r'/videos?/(\d+)', video_url)
                        if not match:
                            match = re.search(r'/(\d+)', video_url)
                        
                        if not match:
                            continue
                        
                        video_id = match.group(1)
                        
                        # Get title
                        title = link.get_attribute('title') or link.text.strip()
                        if not title or len(title) > 150:
                            continue
                        
                        # Get thumbnail
                        try:
                            img = link.find_element(By.TAG_NAME, 'img')
                            thumbnail = img.get_attribute('src') or img.get_attribute('data-src')
                        except:
                            thumbnail = ''
                        
                        video_data = {
                            'id': f"{site_name.lower()}_{video_id}",
                            'video_id': video_id,
                            'title': title.strip(),
                            'video_url': video_url,
                            'embed_url': embed_pattern.format(id=video_id),
                            'thumbnail': thumbnail,
                            'source': site_name.lower()
                        }
                        
                        videos.append(video_data)
                        page_videos += 1
                        
                    except Exception as e:
                        continue
                
                print(f"  ✓ Scraped {page_videos} videos (Total: {len(videos)})")
                
                if page_videos == 0:
                    break
                
                page += 1
                time.sleep(1)
            
            print(f"✅ {site_name}: {len(videos)} videos scraped")
            return videos
            
        except Exception as e:
            print(f"❌ Error scraping {site_name}: {e}")
            return videos


def main():
    """Test the browser scraper"""
    scraper = UniversalBrowserScraper(headless=True)
    
    # Define sites to scrape
    sites = [
        {
            'base_url': 'https://upornia.com',
            'name': 'Upornia',
            'embed': 'https://upornia.com/embed/{id}',
            'max_videos': 100
        },
        {
            'base_url': 'https://www.drtuber.com',
            'name': 'DrTuber',
            'embed': 'https://www.drtuber.com/embed/{id}',
            'max_videos': 100
        },
        {
            'base_url': 'https://txxx.com',
            'name': 'Txxx',
            'embed': 'https://txxx.com/embed/{id}/',
            'max_videos': 100
        },
    ]
    
    all_videos = []
    
    for site in sites:
        videos = scraper.scrape_site(
            base_url=site['base_url'],
            site_name=site['name'],
            embed_pattern=site['embed'],
            max_videos=site['max_videos']
        )
        all_videos.extend(videos)
        time.sleep(2)
    
    scraper.close_driver()
    
    # Save results
    if all_videos:
        with open('browser_scraped_videos.json', 'w', encoding='utf-8') as f:
            json.dump(all_videos, f, indent=2, ensure_ascii=False)
        print(f"\n🎉 Total: {len(all_videos)} videos saved to browser_scraped_videos.json")
    else:
        print("\n❌ No videos scraped")


if __name__ == "__main__":
    main()
