"""
Master scraper - Run all site scrapers and combine results
"""

import json
import random
from datetime import datetime
from scraper import EpornerScraper
from scraper_txxx import TxxxScraper
from scraper_hellporno import HellPornoScraper
from scraper_hclips import HClipsScraper
from scraper_analdin import AnalDinScraper
from scraper_upornia import UporniaScraper
from scraper_drtuber import DrTuberScraper
from scraper_asianmuffin import AsianMuffinScraper

def main():
    print("="*70)
    print("🚀 MASSIVE MULTI-SITE SCRAPE - 8 SOURCES")
    print("="*70)
    print("\nScraping from 8 different sites for MAXIMUM content!\n")
    
    all_videos = []
    
    # Site 1: Eporner.com
    print("\n" + "="*70)
    print("1️⃣  EPORNER.COM")
    print("="*70)
    try:
        scraper1 = EpornerScraper()
        videos1 = scraper1.scrape_homepage(max_videos=600)
        all_videos.extend(videos1)
        print(f"✅ Eporner: {len(videos1)} videos")
    except Exception as e:
        print(f"❌ Eporner error: {e}")
    
    # Site 2: Txxx.com
    print("\n" + "="*70)
    print("2️⃣  TXXX.COM")
    print("="*70)
    try:
        scraper2 = TxxxScraper()
        videos2 = scraper2.scrape_homepage(max_videos=300)
        all_videos.extend(videos2)
        print(f"✅ Txxx: {len(videos2)} videos")
    except Exception as e:
        print(f"❌ Txxx error: {e}")
    
    # Site 3: HellPorno.com
    print("\n" + "="*70)
    print("3️⃣  HELLPORNO.COM")
    print("="*70)
    try:
        scraper3 = HellPornoScraper()
        videos3 = scraper3.scrape_homepage(max_videos=300)
        all_videos.extend(videos3)
        print(f"✅ HellPorno: {len(videos3)} videos")
    except Exception as e:
        print(f"❌ HellPorno error: {e}")
    
    # Site 4: HClips.com
    print("\n" + "="*70)
    print("4️⃣  HCLIPS.COM")
    print("="*70)
    try:
        scraper4 = HClipsScraper()
        videos4 = scraper4.scrape_homepage(max_videos=300)
        all_videos.extend(videos4)
        print(f"✅ HClips: {len(videos4)} videos")
    except Exception as e:
        print(f"❌ HClips error: {e}")
    
    # Site 5: AnalDin.com
    print("\n" + "="*70)
    print("5️⃣  ANALDIN.COM")
    print("="*70)
    try:
        scraper5 = AnalDinScraper()
        videos5 = scraper5.scrape_homepage(max_videos=300)
        all_videos.extend(videos5)
        print(f"✅ AnalDin: {len(videos5)} videos")
    except Exception as e:
        print(f"❌ AnalDin error: {e}")
    
    # Site 6: Upornia.com
    print("\n" + "="*70)
    print("6️⃣  UPORNIA.COM")
    print("="*70)
    try:
        scraper6 = UporniaScraper()
        videos6 = scraper6.scrape_homepage(max_videos=300)
        all_videos.extend(videos6)
        print(f"✅ Upornia: {len(videos6)} videos")
    except Exception as e:
        print(f"❌ Upornia error: {e}")
    
    # Site 7: DrTuber.com
    print("\n" + "="*70)
    print("7️⃣  DRTUBER.COM")
    print("="*70)
    try:
        scraper7 = DrTuberScraper()
        videos7 = scraper7.scrape_homepage(max_videos=300)
        all_videos.extend(videos7)
        print(f"✅ DrTuber: {len(videos7)} videos")
    except Exception as e:
        print(f"❌ DrTuber error: {e}")
    
    # Site 8: AsianMuffin.com
    print("\n" + "="*70)
    print("8️⃣  ASIANMUFFIN.COM")
    print("="*70)
    try:
        scraper8 = AsianMuffinScraper()
        videos8 = scraper8.scrape_homepage(max_videos=500)
        all_videos.extend(videos8)
        print(f"✅ AsianMuffin: {len(videos8)} videos")
    except Exception as e:
        print(f"❌ AsianMuffin error: {e}")
    
    # Shuffle videos for variety
    random.shuffle(all_videos)
    
    # Save combined results
    print("\n" + "="*70)
    print("💾 SAVING COMBINED RESULTS")
    print("="*70)
    
    with open('scraped_videos.json', 'w', encoding='utf-8') as f:
        json.dump(all_videos, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 SUCCESS!")
    print(f"="*70)
    print(f"Total Videos Scraped: {len(all_videos)}")
    print(f"Saved to: scraped_videos.json")
    print(f"="*70)
    
    # Show breakdown by source
    print(f"\n📊 Breakdown by Source:")
    sources = {}
    for video in all_videos:
        source = video.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count} videos")
    
    print(f"\n✅ Ready to load into Blue Tube!")
    print(f"Run: python load_videos.py")

if __name__ == "__main__":
    main()
