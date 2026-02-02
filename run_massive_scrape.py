"""
Quick script to run massive scraping with preset values
This will scrape 800 videos from each of 15 sources = ~12,000 total videos
"""

from enhanced_scraper import EnhancedVideoScraper
import sys

def main():
    print("\n" + "="*60)
    print("🚀 AUTOMATED MASSIVE SCRAPING - 10,000+ VIDEOS")
    print("="*60)
    print("Configuration:")
    print("  - 15 video sources")
    print("  - 800 videos per source")
    print("  - Target: ~12,000 total videos")
    print("="*60 + "\n")
    
    try:
        # Create scraper instance
        print("Initializing scraper...")
        scraper = EnhancedVideoScraper()
        
        # Display current stats
        stats = scraper.get_statistics()
        print(f"📊 Current Database: {stats['total_videos']:,} videos\n")
        
        # Start massive scraping with 2000 videos per source
        print("Starting scraping operation...")
        print("This will take approximately 60-90 minutes.")
        print("Please wait...\n")
        
        scraper.scrape_massive_collection(videos_per_source=2000)
        
        # Display final stats
        final_stats = scraper.get_statistics()
        print(f"\n{'='*60}")
        print(f"✅ SCRAPING COMPLETE!")
        print(f"{'='*60}")
        print(f"📊 Total Videos: {final_stats['total_videos']:,}")
        print(f"📁 Database: video_database.json")
        print(f"\nNext step: Run 'python app.py' to start the server!")
        print(f"{'='*60}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        print("Progress has been saved to video_database.json")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during scraping: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
