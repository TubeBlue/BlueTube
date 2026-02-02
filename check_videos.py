import json

with open('video_cache.json', 'r', encoding='utf-8') as f:
    cache = json.load(f)
    print(f"✅ Cache contains: {len(cache['videos'])} videos")
    
    # Count by source
    sources = {}
    for v in cache['videos']:
        source = v.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print("\n📊 By source:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count}")
