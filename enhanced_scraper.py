"""
Enhanced Multi-Source Video Scraper
Scrapes thousands of videos from multiple sources with pagination
"""

import json
import os
from datetime import datetime
from scraper import EpornerScraper
from scraper_xvideos import XVideosScraper
from scraper_xnxx import XNXXScraper
from scraper_youporn import YouPornScraper
from scraper_fapality import FapalityScraper
from scraper_momvids import MomVidsScraper
from scraper_erome import EromeScraper
from scraper_darknessporn import DarknessPornScraper
from scraper_analdin import AnalDinScraper
from scraper_asianmuffin import AsianMuffinScraper
from scraper_drtuber import DrTuberScraper
from scraper_hclips import HClipsScraper
from scraper_hellporno import HellPornoScraper
from scraper_txxx import TxxxScraper
from scraper_upornia import UporniaScraper
import time


class EnhancedVideoScraper:
    """Enhanced scraper that collects massive amounts of videos"""
    
    def __init__(self):
        self.scrapers = {
            'eporner': EpornerScraper(),
            'xvideos': XVideosScraper(),
            'xnxx': XNXXScraper(),
            'youporn': YouPornScraper(),
            'fapality': FapalityScraper(),
            'momvids': MomVidsScraper(),
            'erome': EromeScraper(),
            'darknessporn': DarknessPornScraper(),
            'analdin': AnalDinScraper(),
            'asianmuffin': AsianMuffinScraper(),
            'drtuber': DrTuberScraper(),
            'hclips': HClipsScraper(),
            'hellporno': HellPornoScraper(),
            'txxx': TxxxScraper(),
            'upornia': UporniaScraper()
        }
        
        self.video_database = 'video_database.json'
        self.all_videos = []
        self.load_database()
    
    def load_database(self):
        """Load existing video database"""
        if os.path.exists(self.video_database):
            try:
                with open(self.video_database, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.all_videos = data.get('videos', [])
                    print(f"📚 Loaded {len(self.all_videos)} videos from database")
            except Exception as e:
                print(f"Error loading database: {e}")
                self.all_videos = []
        else:
            self.all_videos = []
    
    def save_database(self):
        """Save video database"""
        try:
            data = {
                'videos': self.all_videos,
                'total_count': len(self.all_videos),
                'last_updated': datetime.now().isoformat(),
                'sources': list(self.scrapers.keys())
            }
            
            with open(self.video_database, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved {len(self.all_videos)} videos to database")
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def scrape_massive_collection(self, videos_per_source=1000):
        """
        Scrape a massive collection of videos from all sources
        
        Args:
            videos_per_source: Number of videos to scrape from each source
        """
        print(f"\n{'='*60}")
        print(f"🚀 MASSIVE SCRAPING OPERATION STARTED")
        print(f"{'='*60}")
        print(f"Target: {videos_per_source} videos per source")
        print(f"Sources: {len(self.scrapers)}")
        print(f"Total Target: {videos_per_source * len(self.scrapers):,} videos")
        print(f"{'='*60}\n")
        
        total_scraped = 0
        
        for source_name, scraper in self.scrapers.items():
            print(f"\n🎬 Scraping from {source_name.upper()}...")
            print(f"{'─'*50}")
            
            try:
                # Scrape videos
                videos = scraper.scrape_homepage(max_videos=videos_per_source)
                
                if videos:
                    # Add source timestamp
                    for video in videos:
                        video['scraped_at'] = datetime.now().isoformat()
                        video['source_name'] = source_name
                    
                    # Remove duplicates by checking video_url
                    existing_urls = {v.get('video_url') for v in self.all_videos}
                    new_videos = [v for v in videos if v.get('video_url') not in existing_urls]
                    
                    self.all_videos.extend(new_videos)
                    total_scraped += len(new_videos)
                    
                    print(f"✅ {source_name}: Scraped {len(videos)} videos ({len(new_videos)} new)")
                else:
                    print(f"❌ {source_name}: No videos found")
                
                # Small delay between sources to be respectful
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ {source_name} error: {e}")
                continue
        
        # Save to database
        self.save_database()
        
        print(f"\n{'='*60}")
        print(f"🎉 SCRAPING COMPLETED!")
        print(f"{'='*60}")
        print(f"📊 Total videos in database: {len(self.all_videos):,}")
        print(f"🆕 New videos added: {total_scraped:,}")
        print(f"📁 Database file: {self.video_database}")
        print(f"{'='*60}\n")
        
        return self.all_videos
    
    def get_random_videos(self, count=100):
        """Get random videos from the database"""
        import random
        if len(self.all_videos) <= count:
            return self.all_videos
        return random.sample(self.all_videos, count)
    
    def get_videos_by_source(self, source_name, count=50):
        """Get videos from a specific source"""
        source_videos = [v for v in self.all_videos if v.get('source') == source_name]
        return source_videos[:count]
    
    def search_videos(self, query, max_results=100):
        """Search videos by title"""
        query_lower = query.lower()
        results = [
            v for v in self.all_videos 
            if query_lower in v.get('title', '').lower()
        ]
        return results[:max_results]
    
    def get_statistics(self):
        """Get database statistics"""
        stats = {
            'total_videos': len(self.all_videos),
            'by_source': {}
        }
        
        for source in self.scrapers.keys():
            count = len([v for v in self.all_videos if v.get('source') == source])
            stats['by_source'][source] = count
        
        return stats


def main():
    """Main scraping function"""
    scraper = EnhancedVideoScraper()
    
    # Display current stats
    stats = scraper.get_statistics()
    print(f"\n📊 Current Database Statistics:")
    print(f"Total Videos: {stats['total_videos']:,}")
    print(f"\nBy Source:")
    for source, count in stats['by_source'].items():
        print(f"  {source.ljust(15)}: {count:,} videos")
    
    # Ask user how many videos to scrape per source
    print(f"\n{'='*60}")
    print(f"How many videos to scrape from each source?")
    print(f"Recommended options:")
    print(f"  100   - Quick test (~1,500 total videos)")
    print(f"  500   - Medium collection (~7,500 total videos)")
    print(f"  700   - 10K+ collection (~10,500 total videos)")
    print(f"  1000  - Large collection (~15,000 total videos)")
    print(f"  3000  - Massive collection (~45,000 total videos)")
    print(f"  5000  - Ultra collection (~75,000 total videos)")
    print(f"  10000 - Mega collection (~150,000+ total videos)")
    print(f"{'='*60}")
    
    try:
        videos_per_source = int(input("\nEnter number (default 1000): ") or "1000")
    except:
        videos_per_source = 1000
    
    # Start scraping
    scraper.scrape_massive_collection(videos_per_source=videos_per_source)
    
    # Display final stats
    final_stats = scraper.get_statistics()
    print(f"\n{'='*60}")
    print(f"📊 FINAL DATABASE STATISTICS")
    print(f"{'='*60}")
    print(f"Total Videos: {final_stats['total_videos']:,}")
    print(f"\nBreakdown by Source:")
    for source, count in sorted(final_stats['by_source'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {source.ljust(15)}: {count:,} videos")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
