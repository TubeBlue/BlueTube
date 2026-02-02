import json
import os

if os.path.exists('video_database.json'):
    with open('video_database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        videos = data.get('videos', [])
        
        print(f"\n{'='*60}")
        print("Sample Video Data - First 5 videos")
        print(f"{'='*60}\n")
        
        for i, video in enumerate(videos[:5]):
            print(f"Video {i+1}:")
            print(f"  Title: {video.get('title', 'N/A')}")
            print(f"  Views: {video.get('views', 'MISSING')}")
            print(f"  Duration: {video.get('duration', 'N/A')}")
            print(f"  Source: {video.get('source_name', video.get('source', 'N/A'))}")
            print(f"  Keys: {list(video.keys())}")
            print()
        
        # Check how many videos have views
        with_views = sum(1 for v in videos if v.get('views') and v.get('views') != 'N/A')
        print(f"{'='*60}")
        print(f"Videos with views data: {with_views} / {len(videos)}")
        print(f"Percentage: {(with_views/len(videos)*100):.1f}%")
        print(f"{'='*60}\n")
else:
    print("No database found.")
