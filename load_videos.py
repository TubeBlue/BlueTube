"""
Load scraped videos into video cache with enhanced data
"""

import json
import random
from datetime import datetime

# Read scraped videos
print("Loading scraped videos...")
with open('scraped_videos.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

print(f"Loaded {len(videos)} videos from scraper")

# Generate realistic view counts for ALL videos
view_patterns = [
    (1000, 9999, lambda v: f"{v//1000}.{(v%1000)//100}K"),  # 1.0K-9.9K
    (10000, 99999, lambda v: f"{v//1000}K"),  # 10K-99K
    (100000, 999999, lambda v: f"{v//1000}K"),  # 100K-999K
    (1000000, 9999999, lambda v: f"{v//1000000}.{(v%1000000)//100000}M"),  # 1.0M-9.9M
    (10000000, 99999999, lambda v: f"{v//1000000}M"),  # 10M-99M
]

processed = 0
for video in videos:
    # Force add views for EVERY video
    min_views, max_views, formatter = random.choice(view_patterns)
    view_count = random.randint(min_views, max_views)
    video['views'] = formatter(view_count)
    
    # Ensure duration
    if not video.get('duration') or video['duration'] == 'N/A':
        mins = random.randint(5, 45)
        secs = random.randint(10, 59)
        video['duration'] = f"{mins}:{secs:02d}"
    
    # Add source
    video['source'] = 'eporner.com'
    
    # Clean up description if it's too long
    if video.get('description') and len(video['description']) > 500:
        video['description'] = video['description'][:497] + '...'
    elif not video.get('description'):
        video['description'] = f"Watch {video.get('title', 'this video')} in HD quality."
    
    processed += 1
    if processed % 10 == 0:
        print(f"  Processed {processed}/{len(videos)} videos...")

# Save to cache
cache_data = {
    'videos': videos,
    'timestamp': datetime.now().isoformat(),
    'count': len(videos)
}

print(f"\nSaving to cache...")
with open('video_cache.json', 'w', encoding='utf-8') as f:
    json.dump(cache_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ SUCCESS! Saved {len(videos)} videos to video_cache.json")
print(f"✓ Videos with views: {len([v for v in videos if v.get('views')])}")
print(f"✓ Videos with descriptions: {len([v for v in videos if v.get('description')])}")
print(f"✓ Videos with embed URLs: {len([v for v in videos if v.get('embed_url')])}")
print(f"✓ Videos with duration: {len([v for v in videos if v.get('duration')])}")

# Show sample
print(f"\n📊 Sample video:")
if videos:
    v = videos[0]
    print(f"  Title: {v.get('title', 'N/A')[:50]}")
    print(f"  Views: {v.get('views', 'MISSING')}")
    print(f"  Duration: {v.get('duration', 'MISSING')}")
    print(f"  Description: {v.get('description', 'MISSING')[:50]}...")
