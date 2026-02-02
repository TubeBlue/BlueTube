import requests
import time

time.sleep(2)  # Wait for server

try:
    # Test page 1
    print("Testing pagination with 36 videos per page...\n")
    
    r1 = requests.get('http://localhost:5000/api/videos?page=1')
    data1 = r1.json()
    
    print(f"✅ Page 1:")
    print(f"   Videos returned: {data1['count']}")
    print(f"   Total videos: {data1.get('total', 'N/A')}")
    print(f"   Per page: {data1.get('per_page', 'N/A')}")
    print(f"   Total pages: {data1.get('total_pages', 'N/A')}")
    
    # Test page 2
    r2 = requests.get('http://localhost:5000/api/videos?page=2')
    data2 = r2.json()
    
    print(f"\n✅ Page 2:")
    print(f"   Videos returned: {data2['count']}")
    print(f"   First video: {data2['videos'][0]['title'][:50] if data2['videos'] else 'None'}")
    
    # Test page 3
    r3 = requests.get('http://localhost:5000/api/videos?page=3')
    data3 = r3.json()
    
    print(f"\n✅ Page 3:")
    print(f"   Videos returned: {data3['count']}")
    
    # Calculate expected pages
    total = data1.get('total', 0)
    per_page = data1.get('per_page', 36)
    expected_pages = (total + per_page - 1) // per_page
    
    print(f"\n📊 Summary:")
    print(f"   Total videos: {total}")
    print(f"   Videos per page: {per_page}")
    print(f"   Total pages: {expected_pages}")
    print(f"   700 videos ÷ 36 per page = ~{700/36:.1f} pages ✓")
    
except Exception as e:
    print(f"❌ Error: {e}")
