import requests
import json

try:
    print("Testing API for views...")
    response = requests.get('http://localhost:5000/api/videos?per_page=5')
    
    if response.status_code == 200:
        data = response.json()
        videos = data.get('videos', [])
        
        print(f"\n✅ API Response OK - {len(videos)} videos received\n")
        
        for i, video in enumerate(videos[:5]):
            print(f"Video {i+1}:")
            print(f"  Title: {video.get('title', 'N/A')[:50]}...")
            print(f"  Views: {video.get('views', 'MISSING')}")
            print(f"  Duration: {video.get('duration', 'N/A')}")
            print()
        
        # Check views percentage
        with_views = sum(1 for v in videos if v.get('views') and v.get('views') != 'N/A')
        print(f"Videos with views: {with_views}/{len(videos)} ({with_views/len(videos)*100:.0f}%)")
    else:
        print(f"❌ API Error: Status {response.status_code}")
        print(f"Server might not be running on http://localhost:5000")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to server")
    print("Please start the server with: python app.py")
except Exception as e:
    print(f"❌ Error: {e}")
