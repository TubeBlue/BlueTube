import json
import os

if os.path.exists('video_database.json'):
    with open('video_database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"\n{'='*60}")
        print(f"📊 VIDEO DATABASE STATUS")
        print(f"{'='*60}")
        print(f"Total Videos: {data['total_count']:,}")
        print(f"Last Updated: {data.get('last_updated', 'N/A')}")
        print(f"Sources: {len(data.get('sources', []))}")
        print(f"{'='*60}\n")
else:
    print("No database found yet.")
