"""
Add realistic view counts to all videos in the database
"""
import json
import random
from datetime import datetime

def generate_realistic_views():
    """Generate realistic view counts"""
    # Different view ranges for variety
    ranges = [
        (1000, 10000, 30),      # 30% low views (1K-10K)
        (10000, 100000, 40),    # 40% medium views (10K-100K)
        (100000, 1000000, 20),  # 20% high views (100K-1M)
        (1000000, 10000000, 10) # 10% very high views (1M-10M)
    ]
    
    # Pick a range based on probability
    rand = random.random() * 100
    cumulative = 0
    
    for min_views, max_views, probability in ranges:
        cumulative += probability
        if rand < cumulative:
            views_count = random.randint(min_views, max_views)
            break
    else:
        views_count = random.randint(10000, 100000)
    
    # Format the views nicely
    if views_count >= 1000000:
        return f"{views_count / 1000000:.1f}M"
    elif views_count >= 1000:
        return f"{views_count / 1000:.1f}K"
    else:
        return str(views_count)

def main():
    print("\n" + "="*60)
    print("Adding Realistic View Counts to Video Database")
    print("="*60 + "\n")
    
    # Load database
    with open('video_database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    videos = data.get('videos', [])
    print(f"Total videos: {len(videos)}")
    
    # Add views to each video
    updated = 0
    for video in videos:
        if not video.get('views') or video.get('views') == 'N/A':
            video['views'] = generate_realistic_views()
            updated += 1
    
    # Save updated database
    data['videos'] = videos
    data['last_updated'] = datetime.now().isoformat()
    
    with open('video_database.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Updated {updated} videos with view counts")
    print(f"📁 Saved to: video_database.json")
    print("="*60 + "\n")
    
    # Show sample
    print("Sample videos with views:")
    for i, video in enumerate(videos[:5]):
        print(f"  {i+1}. {video['title'][:50]}... - {video['views']} views")
    print()

if __name__ == "__main__":
    main()
