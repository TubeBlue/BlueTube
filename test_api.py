import requests
import time

time.sleep(3)  # Wait for server

try:
    r = requests.get('http://localhost:5000/api/videos')
    data = r.json()
    print(f"✅ Server is running!")
    print(f"📊 Videos loaded: {data.get('count', 0)}")
    print(f"📄 Total videos: {data.get('total', 0)}")
    
    if data.get('videos'):
        v = data['videos'][0]
        print(f"\n📹 Sample video:")
        print(f"  Title: {v.get('title', 'N/A')[:50]}")
        print(f"  Views: {v.get('views', 'MISSING')}")
        print(f"  Duration: {v.get('duration', 'MISSING')}")
except Exception as e:
    print(f"❌ Error: {e}")
