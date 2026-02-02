"""
Blue Tube - Flask Backend API
Serves scraped video data to the frontend
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
from scraper import EpornerScraper
from scraper_xvideos import XVideosScraper
from scraper_xnxx import XNXXScraper
from scraper_youporn import YouPornScraper
from scraper_fapality import FapalityScraper
from scraper_momvids import MomVidsScraper
from scraper_erome import EromeScraper
from scraper_darknessporn import DarknessPornScraper
from scraper_analdin import AnalDinScraper
from scraper_asianmuffin import AsianMuffinScraper
from scraper_drtuber import DrTuberScraper
from scraper_hclips import HClipsScraper
from scraper_hellporno import HellPornoScraper
from scraper_txxx import TxxxScraper
from scraper_upornia import UporniaScraper
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
CACHE_FILE = 'video_cache.json'
VIDEO_DATABASE = 'video_database.json'
CACHE_DURATION = timedelta(hours=1)  # Cache videos for 1 hour

# Global variables
cached_videos = []
all_videos = []  # Large video database
cache_timestamp = None
eporner_scraper = EpornerScraper()
xvideos_scraper = XVideosScraper()
xnxx_scraper = XNXXScraper()
youporn_scraper = YouPornScraper()
fapality_scraper = FapalityScraper()
momvids_scraper = MomVidsScraper()
erome_scraper = EromeScraper()
darknessporn_scraper = DarknessPornScraper()
analdin_scraper = AnalDinScraper()
asianmuffin_scraper = AsianMuffinScraper()
drtuber_scraper = DrTuberScraper()
hclips_scraper = HClipsScraper()
hellporno_scraper = HellPornoScraper()
txxx_scraper = TxxxScraper()
upornia_scraper = UporniaScraper()
is_scraping = False


def load_cache():
    """Load cached videos from file"""
    global cached_videos, cache_timestamp
    
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cached_videos = data.get('videos', [])
                cache_timestamp = datetime.fromisoformat(data.get('timestamp', datetime.min.isoformat()))
                print(f"Loaded {len(cached_videos)} videos from cache")
                return True
        except Exception as e:
            print(f"Error loading cache: {e}")
    
    return False


def load_video_database():
    """Load the large video database"""
    global all_videos
    
    if os.path.exists(VIDEO_DATABASE):
        try:
            with open(VIDEO_DATABASE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_videos = data.get('videos', [])
                print(f"📚 Loaded {len(all_videos):,} videos from database")
                return True
        except Exception as e:
            print(f"Error loading video database: {e}")
    
    print("No video database found. Run enhanced_scraper.py to build it.")
    return False


def save_cache(videos):
    """Save videos to cache file"""
    global cached_videos, cache_timestamp
    
    try:
        cached_videos = videos
        cache_timestamp = datetime.now()
        
        data = {
            'videos': videos,
            'timestamp': cache_timestamp.isoformat()
        }
        
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(videos)} videos to cache")
        return True
    except Exception as e:
        print(f"Error saving cache: {e}")
        return False


def is_cache_valid():
    """Check if cache is still valid"""
    if not cached_videos or cache_timestamp is None:
        return False
    
    return datetime.now() - cache_timestamp < CACHE_DURATION


def scrape_videos_background():
    """Scrape videos from all sources in background thread"""
    global is_scraping, cached_videos
    
    is_scraping = True
    print("🚀 Starting background scraping from 15 video sources...")
    
    try:
        all_videos = []
        
        # Scrape from Eporner (50 videos)
        print("📡 Scraping from Eporner...")
        try:
            eporner_videos = eporner_scraper.scrape_homepage(max_videos=50)
            if eporner_videos:
                all_videos.extend(eporner_videos)
                print(f"✅ Got {len(eporner_videos)} videos from Eporner")
        except Exception as e:
            print(f"❌ Eporner error: {e}")
        
        # Scrape from XVideos (50 videos)
        print("📡 Scraping from XVideos...")
        try:
            xvideos_videos = xvideos_scraper.scrape_homepage(max_videos=50)
            if xvideos_videos:
                all_videos.extend(xvideos_videos)
                print(f"✅ Got {len(xvideos_videos)} videos from XVideos")
        except Exception as e:
            print(f"❌ XVideos error: {e}")
        
        # Scrape from XNXX (50 videos)
        print("📡 Scraping from XNXX...")
        try:
            xnxx_videos = xnxx_scraper.scrape_homepage(max_videos=50)
            if xnxx_videos:
                all_videos.extend(xnxx_videos)
                print(f"✅ Got {len(xnxx_videos)} videos from XNXX")
        except Exception as e:
            print(f"❌ XNXX error: {e}")
        
        # Scrape from YouPorn (50 videos)
        print("📡 Scraping from YouPorn...")
        try:
            youporn_videos = youporn_scraper.scrape_homepage(max_videos=50)
            if youporn_videos:
                all_videos.extend(youporn_videos)
                print(f"✅ Got {len(youporn_videos)} videos from YouPorn")
        except Exception as e:
            print(f"❌ YouPorn error: {e}")
        
        # Scrape from Fapality (50 videos)
        print("📡 Scraping from Fapality...")
        try:
            fapality_videos = fapality_scraper.scrape_homepage(max_videos=50)
            if fapality_videos:
                all_videos.extend(fapality_videos)
                print(f"✅ Got {len(fapality_videos)} videos from Fapality")
        except Exception as e:
            print(f"❌ Fapality error: {e}")
        
        # Scrape from MomVids (50 videos)
        print("📡 Scraping from MomVids...")
        try:
            momvids_videos = momvids_scraper.scrape_homepage(max_videos=50)
            if momvids_videos:
                all_videos.extend(momvids_videos)
                print(f"✅ Got {len(momvids_videos)} videos from MomVids")
        except Exception as e:
            print(f"❌ MomVids error: {e}")
        
        # Scrape from Erome (50 videos)
        print("📡 Scraping from Erome...")
        try:
            erome_videos = erome_scraper.scrape_homepage(max_videos=50)
            if erome_videos:
                all_videos.extend(erome_videos)
                print(f"✅ Got {len(erome_videos)} videos from Erome")
        except Exception as e:
            print(f"❌ Erome error: {e}")
        
        # Scrape from DarknessPorn (50 videos)
        print("📡 Scraping from DarknessPorn...")
        try:
            darknessporn_videos = darknessporn_scraper.scrape_homepage(max_videos=50)
            if darknessporn_videos:
                all_videos.extend(darknessporn_videos)
                print(f"✅ Got {len(darknessporn_videos)} videos from DarknessPorn")
        except Exception as e:
            print(f"❌ DarknessPorn error: {e}")
        
        # Scrape from Analdin (50 videos)
        print("📡 Scraping from Analdin...")
        try:
            analdin_videos = analdin_scraper.scrape_homepage(max_videos=50)
            if analdin_videos:
                all_videos.extend(analdin_videos)
                print(f"✅ Got {len(analdin_videos)} videos from Analdin")
        except Exception as e:
            print(f"❌ Analdin error: {e}")
        
        # Scrape from AsianMuffin (50 videos)
        print("📡 Scraping from AsianMuffin...")
        try:
            asianmuffin_videos = asianmuffin_scraper.scrape_homepage(max_videos=50)
            if asianmuffin_videos:
                all_videos.extend(asianmuffin_videos)
                print(f"✅ Got {len(asianmuffin_videos)} videos from AsianMuffin")
        except Exception as e:
            print(f"❌ AsianMuffin error: {e}")
        
        # Scrape from DrTuber (50 videos)
        print("📡 Scraping from DrTuber...")
        try:
            drtuber_videos = drtuber_scraper.scrape_homepage(max_videos=50)
            if drtuber_videos:
                all_videos.extend(drtuber_videos)
                print(f"✅ Got {len(drtuber_videos)} videos from DrTuber")
        except Exception as e:
            print(f"❌ DrTuber error: {e}")
        
        # Scrape from HClips (50 videos)
        print("📡 Scraping from HClips...")
        try:
            hclips_videos = hclips_scraper.scrape_homepage(max_videos=50)
            if hclips_videos:
                all_videos.extend(hclips_videos)
                print(f"✅ Got {len(hclips_videos)} videos from HClips")
        except Exception as e:
            print(f"❌ HClips error: {e}")
        
        # Scrape from HellPorno (50 videos)
        print("📡 Scraping from HellPorno...")
        try:
            hellporno_videos = hellporno_scraper.scrape_homepage(max_videos=50)
            if hellporno_videos:
                all_videos.extend(hellporno_videos)
                print(f"✅ Got {len(hellporno_videos)} videos from HellPorno")
        except Exception as e:
            print(f"❌ HellPorno error: {e}")
        
        # Scrape from Txxx (50 videos)
        print("📡 Scraping from Txxx...")
        try:
            txxx_videos = txxx_scraper.scrape_homepage(max_videos=50)
            if txxx_videos:
                all_videos.extend(txxx_videos)
                print(f"✅ Got {len(txxx_videos)} videos from Txxx")
        except Exception as e:
            print(f"❌ Txxx error: {e}")
        
        # Scrape from Upornia (50 videos)
        print("📡 Scraping from Upornia...")
        try:
            upornia_videos = upornia_scraper.scrape_homepage(max_videos=50)
            if upornia_videos:
                all_videos.extend(upornia_videos)
                print(f"✅ Got {len(upornia_videos)} videos from Upornia")
        except Exception as e:
            print(f"❌ Upornia error: {e}")
        
        if all_videos:
            save_cache(all_videos)
            print(f"🎉 Background scraping completed: {len(all_videos)} total videos from 15 sources!")
        else:
            print("⚠️ Background scraping completed but no videos found")
    except Exception as e:
        print(f"❌ Error in background scraping: {e}")
    finally:
        is_scraping = False


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', path)


@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        'message': 'Blue Tube API',
        'version': '2.0',
        'endpoints': {
            '/api/videos': 'Get all videos',
            '/api/videos/<video_id>': 'Get specific video',
            '/api/search?q=<query>': 'Search videos',
            '/api/categories': 'Get all categories/tags',
            '/api/categories/<category>': 'Get videos by category',
            '/api/trending': 'Get trending videos',
            '/api/status': 'Get API status'
        }
    })


@app.route('/api/status')
def status():
    """Get API status"""
    return jsonify({
        'success': True,
        'status': 'online',
        'cached_videos': len(cached_videos),
        'total_videos_in_database': len(all_videos),
        'cache_valid': is_cache_valid(),
        'cache_age': str(datetime.now() - cache_timestamp) if cache_timestamp else 'N/A',
        'is_scraping': is_scraping
    })


@app.route('/api/videos')
def get_videos():
    """Get videos with pagination support"""
    global cached_videos, all_videos, is_scraping
    
    # Get pagination parameters - DEFAULT TO 36 PER PAGE
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 36))
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    # Use database if available (for massive collections)
    if all_videos:
        # Calculate pagination
        total = len(all_videos)
        start = (page - 1) * per_page
        end = start + per_page
        
        # Get paginated videos
        videos = all_videos[start:end]
        
        return jsonify({
            'success': True,
            'videos': videos,
            'count': len(videos),
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'source': 'database'
        })
    
    # Fallback to regular scraping if no database
    if force_refresh or not is_cache_valid():
        if not is_scraping:
            thread = threading.Thread(target=scrape_videos_background)
            thread.daemon = True
            thread.start()
            time.sleep(0.5)
    
    if cached_videos:
        # Calculate pagination for cached videos
        total = len(cached_videos)
        start = (page - 1) * per_page
        end = start + per_page
        
        # Get paginated videos
        paginated_videos = cached_videos[start:end]
        
        return jsonify({
            'success': True,
            'videos': paginated_videos,
            'count': len(paginated_videos),
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'cached': is_cache_valid(),
            'is_scraping': is_scraping,
            'source': 'cache'
        })
    else:
        if is_scraping:
            return jsonify({
                'success': True,
                'videos': [],
                'count': 0,
                'message': 'Scraping in progress, please wait...',
                'is_scraping': True
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No videos available. Run enhanced_scraper.py to build database.',
                'videos': [],
                'count': 0
            }), 404


@app.route('/api/videos/<video_id>')
def get_video(video_id):
    """Get a specific video by ID"""
    if not cached_videos:
        return jsonify({
            'success': False,
            'error': 'No videos available'
        }), 404
    
    # Find video by ID
    video = next((v for v in cached_videos if v.get('id') == video_id), None)
    
    if video:
        return jsonify({
            'success': True,
            'video': video
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Video not found'
        }), 404


@app.route('/api/search')
def search_videos():
    """Search videos"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query is required'
        }), 400
    
    # Search in all videos if database available
    if all_videos:
        results = [
            v for v in all_videos 
            if query.lower() in v.get('title', '').lower()
        ][:100]  # Limit to 100 results
        
        return jsonify({
            'success': True,
            'videos': results,
            'count': len(results),
            'query': query
        })
    
    # Search in cached videos
    if cached_videos:
        results = [
            v for v in cached_videos 
            if query.lower() in v.get('title', '').lower()
        ]
        
        return jsonify({
            'success': True,
            'videos': results,
            'count': len(results),
            'query': query
        })
    
    return jsonify({
        'success': False,
        'error': 'No videos available'
    }), 404


@app.route('/api/categories')
def get_categories():
    """Get all available categories/tags"""
    categories = [
        {'id': 'asian', 'name': 'Asian', 'icon': '🎌'},
        {'id': 'milf', 'name': 'MILF', 'icon': '👩'},
        {'id': 'teen', 'name': 'Teen', 'icon': '👧'},
        {'id': 'latina', 'name': 'Latina', 'icon': '💃'},
        {'id': 'ebony', 'name': 'Ebony', 'icon': '🖤'},
        {'id': 'blonde', 'name': 'Blonde', 'icon': '👱‍♀️'},
        {'id': 'brunette', 'name': 'Brunette', 'icon': '👩‍🦰'},
        {'id': 'amateur', 'name': 'Amateur', 'icon': '🎥'},
        {'id': 'anal', 'name': 'Anal', 'icon': '🍑'},
        {'id': 'blowjob', 'name': 'Blowjob', 'icon': '💋'},
        {'id': 'creampie', 'name': 'Creampie', 'icon': '💦'},
        {'id': 'cumshot', 'name': 'Cumshot', 'icon': '💥'},
        {'id': 'big-tits', 'name': 'Big Tits', 'icon': '🔥'},
        {'id': 'big-ass', 'name': 'Big Ass', 'icon': '🍑'},
        {'id': 'threesome', 'name': 'Threesome', 'icon': '👥'},
        {'id': 'lesbian', 'name': 'Lesbian', 'icon': '💕'},
        {'id': 'hardcore', 'name': 'Hardcore', 'icon': '⚡'},
        {'id': 'pov', 'name': 'POV', 'icon': '👁️'},
        {'id': 'hd', 'name': 'HD/4K', 'icon': '📺'},
        {'id': 'outdoor', 'name': 'Outdoor', 'icon': '🌳'},
    ]
    
    return jsonify({
        'success': True,
        'categories': categories,
        'count': len(categories)
    })


@app.route('/api/categories/<category_id>')
def get_category_videos(category_id):
    """Get videos for a specific category/tag"""
    # Search by tag in video title or tags field
    if all_videos:
        # Filter videos that contain the category_id in title or tags
        category_name = category_id.lower().replace('-', ' ')
        results = []
        seen_urls = set()  # Track unique video URLs to remove duplicates
        
        for video in all_videos:
            video_url = video.get('video_url')
            
            # Skip if we've already added this video (duplicate check)
            if video_url and video_url in seen_urls:
                continue
            
            title_lower = video.get('title', '').lower()
            tags_lower = video.get('tags', '').lower() if video.get('tags') else ''
            
            # Check if category matches title or tags
            if category_name in title_lower or category_name in tags_lower or category_id in tags_lower:
                results.append(video)
                if video_url:
                    seen_urls.add(video_url)
            
            # Limit to 200 results per category
            if len(results) >= 200:
                break
        
        return jsonify({
            'success': True,
            'videos': results,
            'count': len(results),
            'category': category_id
        })
    
    # Fallback to cached videos
    if cached_videos:
        category_name = category_id.lower().replace('-', ' ')
        results = []
        seen_urls = set()
        
        for video in cached_videos:
            video_url = video.get('video_url')
            
            # Skip duplicates
            if video_url and video_url in seen_urls:
                continue
            
            title_lower = video.get('title', '').lower()
            tags_lower = video.get('tags', '').lower() if video.get('tags') else ''
            
            if category_name in title_lower or category_name in tags_lower or category_id in tags_lower:
                results.append(video)
                if video_url:
                    seen_urls.add(video_url)
        
        return jsonify({
            'success': True,
            'videos': results,
            'count': len(results),
            'category': category_id
        })
    
    return jsonify({
        'success': False,
        'error': 'No videos available',
        'videos': [],
        'count': 0
    }), 404


@app.route('/api/trending')
def get_trending():
    """Get trending videos (most viewed/popular) with pagination"""
    videos_to_use = all_videos if all_videos else cached_videos
    
    if not videos_to_use:
        return jsonify({
            'success': False,
            'error': 'No videos available'
        }), 404
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 200))
    
    # Sort by views if available, otherwise return random videos
    import random
    trending = random.sample(videos_to_use, min(len(videos_to_use), 5000))
    
    # Calculate pagination
    total = len(trending)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_videos = trending[start:end]
    
    return jsonify({
        'success': True,
        'videos': paginated_videos,
        'count': len(paginated_videos),
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })


@app.route('/api/scrape')
def trigger_scrape():
    """Manually trigger scraping"""
    global is_scraping
    
    if is_scraping:
        return jsonify({
            'success': False,
            'message': 'Scraping already in progress'
        })
    
    # Start background scraping
    thread = threading.Thread(target=scrape_videos_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Scraping started in background'
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


def initialize_app():
    """Initialize the application"""
    print("="*60)
    print("🎬 Blue Tube API Server - Multi-Source Video Aggregator")
    print("="*60)
    
    # Try to load video database first
    load_video_database()
    
    # Try to load cache
    if load_cache():
        if is_cache_valid():
            print("Cache is valid, using cached videos")
        else:
            print("Cache is expired, will scrape new videos on first request")
    else:
        print("No cache found, will scrape videos on first request")
    
    print("\nAPI Server is ready!")
    print("Frontend URL: http://localhost:5000")
    print("API URL: http://localhost:5000/api")
    print("="*50)


@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(key in data for key in ['email', 'subject', 'message']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Save contact message to file
        contact_file = 'contact_messages.json'
        
        # Load existing messages
        messages = []
        if os.path.exists(contact_file):
            with open(contact_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
        
        # Add new message
        message_data = {
            'email': data['email'],
            'subject': data['subject'],
            'message': data['message'],
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        messages.append(message_data)
        
        # Save messages
        with open(contact_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        
        print(f"\n📧 New contact message from: {data['email']}")
        print(f"   Subject: {data['subject']}")
        print(f"   Message: {data['message'][:50]}...")
        
        return jsonify({
            'success': True,
            'message': 'Contact message received successfully'
        })
    
    except Exception as e:
        print(f"Error handling contact form: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    initialize_app()
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
