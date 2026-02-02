"""
Update cache from database
"""
import json
import random
from datetime import datetime

# Load database
with open('video_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

videos = data.get('videos', [])

# Select random 64 videos for cache
cache_videos = random.sample(videos, min(64, len(videos)))

# Save to cache
cache_data = {
    'videos': cache_videos,
    'timestamp': datetime.now().isoformat()
}

with open('video_cache.json', 'w', encoding='utf-8') as f:
    json.dump(cache_data, f, indent=2, ensure_ascii=False)

print(f"✅ Updated cache with {len(cache_videos)} videos (all have views)")
