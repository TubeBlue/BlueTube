"""
Filter out hentai and cartoon porn videos
"""

import json
import re

# Keywords that indicate hentai/cartoon/anime content
FILTER_KEYWORDS = [
    'hentai', 'anime', 'cartoon', 'animated', 'animation',
    '3d cartoon', 'toon', 'drawn', 'sfm', 'overwatch',
    'tentacle', 'minecraft', 'fortnite', 'pokemon',
    'naruto', 'dragon ball', 'zelda', 'mario',
    'sonic', 'my little pony', 'mlp', 'furry',
    'yiff', 'anthro', 'kemono', 'doujin',
    'エロアニメ', 'アニメ', 'ヘンタイ',
    'comic', 'manga', 'cg', 'render', '3dcg',
    'sfm porn', 'source filmmaker', 'blender porn'
]

def is_hentai_or_cartoon(video):
    """Check if video appears to be hentai or cartoon"""
    
    # Get text fields to check
    title = video.get('title', '').lower()
    description = video.get('description', '').lower()
    tags = video.get('tags', [])
    if isinstance(tags, str):
        tags = tags.lower()
    elif isinstance(tags, list):
        tags = ' '.join(tags).lower()
    else:
        tags = ''
    
    # Combine all text
    text = f"{title} {description} {tags}"
    
    # Check for keywords
    for keyword in FILTER_KEYWORDS:
        if keyword in text:
            return True
    
    return False

def filter_videos():
    """Filter out hentai and cartoon videos"""
    
    print("Loading video cache...")
    with open('video_cache.json', 'r', encoding='utf-8') as f:
        cache = json.load(f)
    
    videos = cache.get('videos', [])
    original_count = len(videos)
    
    print(f"Original video count: {original_count}")
    print("\nScanning for hentai/cartoon content...")
    
    # Filter videos
    filtered_videos = []
    removed_videos = []
    
    for video in videos:
        if is_hentai_or_cartoon(video):
            removed_videos.append(video)
            print(f"  ❌ Removing: {video.get('title', 'Unknown')[:60]}")
        else:
            filtered_videos.append(video)
    
    # Update cache
    cache['videos'] = filtered_videos
    cache['count'] = len(filtered_videos)
    
    print(f"\n" + "="*70)
    print(f"📊 Filtering Results:")
    print(f"="*70)
    print(f"Original videos: {original_count}")
    print(f"Removed videos: {len(removed_videos)}")
    print(f"Remaining videos: {len(filtered_videos)}")
    print(f"Percentage removed: {len(removed_videos)/original_count*100:.1f}%")
    
    # Save filtered cache
    print(f"\nSaving filtered videos...")
    with open('video_cache.json', 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    
    # Save removed videos list for review
    with open('removed_videos.json', 'w', encoding='utf-8') as f:
        json.dump(removed_videos, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Filtered cache saved to: video_cache.json")
    print(f"📝 Removed videos list saved to: removed_videos.json")
    
    # Show some examples of kept videos
    if filtered_videos:
        print(f"\n✅ Sample of remaining videos:")
        for i, video in enumerate(filtered_videos[:5]):
            print(f"   {i+1}. {video.get('title', 'Unknown')[:60]}")
    
    print(f"\n🎉 Filtering complete!")
    print(f"Restart the server to load the filtered content.")

if __name__ == "__main__":
    filter_videos()
