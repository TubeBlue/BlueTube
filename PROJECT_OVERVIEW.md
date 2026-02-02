# Blue Tube - Project Overview

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                        │
│  ┌────────────────────────────────────────────────┐     │
│  │  index.html (UI) + style.css + script.js       │     │
│  │  - Netflix-style interface                      │     │
│  │  - Video cards with thumbnails                  │     │
│  │  - Search functionality                         │     │
│  │  - Modal video player                           │     │
│  └────────────────────────────────────────────────┘     │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP Requests
                        ↓
┌─────────────────────────────────────────────────────────┐
│               FLASK BACKEND SERVER                       │
│  ┌────────────────────────────────────────────────┐     │
│  │  app.py (API Server)                           │     │
│  │  - /api/videos - Get all videos                │     │
│  │  - /api/search - Search videos                 │     │
│  │  - /api/status - Server status                 │     │
│  │  - Caching system                              │     │
│  └────────────────────┬───────────────────────────┘     │
│                       │ Calls                            │
│                       ↓                                  │
│  ┌────────────────────────────────────────────────┐     │
│  │  scraper.py (Web Scraper)                      │     │
│  │  - Scrapes eporner.com                         │     │
│  │  - Extracts video data                         │     │
│  │  - Generates embed URLs                        │     │
│  └────────────────────┬───────────────────────────┘     │
└────────────────────────┼───────────────────────────────┘
                         │ HTTP Requests
                         ↓
         ┌───────────────────────────────┐
         │    eporner.com (Source)        │
         │    - Video data                │
         │    - Thumbnails                │
         │    - Metadata                  │
         └───────────────────────────────┘
```

## 🗂️ File Structure

```
Blue Tube/
│
├── Frontend Files
│   ├── index.html          # Main HTML page with Netflix-style UI
│   ├── style.css           # All styling (responsive, modern design)
│   └── script.js           # Frontend logic, API calls, video display
│
├── Backend Files
│   ├── app.py              # Flask server with RESTful API
│   ├── scraper.py          # Web scraper for eporner.com
│   └── config.py           # Configuration settings
│
├── Documentation
│   ├── README.md           # Complete documentation
│   ├── QUICK_START.md      # Quick start guide
│   └── PROJECT_OVERVIEW.md # This file
│
├── Configuration
│   ├── requirements.txt    # Python dependencies
│   └── .gitignore         # Git ignore rules
│
└── Scripts
    ├── start.bat          # Windows startup script
    └── start.sh           # Linux/Mac startup script
```

## 🔄 Data Flow

```
1. User opens website (index.html)
   ↓
2. JavaScript (script.js) sends request to Flask API
   ↓
3. Flask (app.py) checks cache
   ↓
4. If cache expired or empty:
   - Call scraper.py
   - Scraper fetches data from eporner.com
   - Extract video info (title, duration, thumbnail, embed URL)
   - Save to cache (video_cache.json)
   ↓
5. Flask returns JSON data to frontend
   ↓
6. JavaScript renders video cards
   ↓
7. User clicks video → Modal opens with iframe player
```

## 🎯 Key Components

### 1. Frontend (index.html + style.css + script.js)

**Features:**
- Netflix-inspired UI with gradient hero section
- Responsive grid layout for video cards
- Search functionality with real-time filtering
- Modal video player with iframe embedding
- Loading states and error handling
- Smooth animations and transitions

**Technologies:**
- Pure HTML5
- CSS3 with flexbox and grid
- Vanilla JavaScript (no frameworks)
- Fetch API for backend communication

### 2. Backend (app.py)

**Features:**
- RESTful API with multiple endpoints
- Smart caching system (1-hour default)
- Background scraping with threading
- CORS enabled for cross-origin requests
- Error handling and logging
- Status monitoring

**Endpoints:**
- `GET /api/videos` - Get all videos
- `GET /api/videos/<id>` - Get specific video
- `GET /api/search?q=query` - Search videos
- `GET /api/status` - Server status
- `GET /api/scrape` - Trigger scraping

**Technologies:**
- Flask (Python web framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- JSON for data storage
- Threading for background tasks

### 3. Scraper (scraper.py)

**Features:**
- Scrapes eporner.com homepage
- Extracts video metadata
- Generates embed URLs
- Search functionality
- Error handling and retries
- Respects rate limits

**Extracted Data:**
- Video title
- Duration
- Thumbnail image
- View count
- Embed URL
- Video page URL

**Technologies:**
- Requests (HTTP library)
- BeautifulSoup4 (HTML parsing)
- Regular expressions for URL parsing

## 🚀 How It Works

### Initial Load

1. **User opens website** → Browser loads `index.html`
2. **Page loads** → `script.js` runs and calls API
3. **API request** → Fetch from `/api/videos`
4. **Backend checks cache** → Load from `video_cache.json`
5. **If cache valid** → Return cached videos
6. **If cache expired** → Trigger scraping in background
7. **Scraper runs** → Fetch data from eporner.com
8. **Parse data** → Extract video information
9. **Save cache** → Store in `video_cache.json`
10. **Return to frontend** → Send JSON response
11. **Render UI** → Display video cards

### User Interaction

**Search:**
1. User types in search box
2. JavaScript filters videos by title
3. Re-render filtered results
4. If no cache, performs live search via API

**Play Video:**
1. User clicks video card
2. Modal opens with video details
3. Iframe loads with embed URL
4. Video plays directly in modal

**Refresh:**
1. User clicks refresh button (↻)
2. Force refresh request sent to API
3. Backend scrapes fresh data
4. New videos displayed

## 📦 Dependencies

### Frontend
- No external dependencies
- Pure vanilla JavaScript
- Google Fonts (Roboto)

### Backend
```
Flask==3.0.0          # Web framework
flask-cors==4.0.0     # CORS support
requests==2.31.0      # HTTP requests
beautifulsoup4==4.12.2 # HTML parsing
lxml==4.9.3           # XML/HTML parser
```

## 🎨 UI Components

### Navigation Bar
- Logo (Blue Tube)
- Menu items (Home, Trending, Categories, My List)
- Search box with icon
- Refresh button

### Hero Section
- Large gradient background
- Featured content title
- Play and Info buttons
- Fade overlay

### Video Grid
- Responsive grid layout
- Video cards with thumbnails
- Hover effects with play icon
- Title and metadata (duration, views)

### Video Modal
- Full-screen overlay
- Close button
- Iframe video player
- Video details (title, duration, views)
- Description area

### Footer
- Copyright notice
- Links (Terms, Privacy, Contact)

## 🔐 Security Considerations

1. **API Keys**: No hardcoded API keys
2. **User Input**: Search queries are sanitized
3. **CORS**: Configurable allowed origins
4. **Rate Limiting**: Respects source website
5. **Error Handling**: Graceful error messages

## ⚡ Performance Optimizations

1. **Caching**: 1-hour cache to reduce scraping
2. **Background Scraping**: Non-blocking scraping
3. **Lazy Loading**: Images load as needed
4. **Responsive Images**: Optimized for different screens
5. **CSS Animations**: GPU-accelerated transforms

## 🧪 Testing

### Test Scraper
```bash
python scraper.py
```
This will scrape 10 videos and save to `scraped_videos.json`.

### Test API
Open in browser:
- http://localhost:5000/api/status
- http://localhost:5000/api/videos
- http://localhost:5000/api/search?q=test

### Test Frontend
1. Start backend: `python app.py`
2. Open `index.html` in browser
3. Check browser console (F12) for errors

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Port in use | Change port in `app.py` |
| No videos | Check backend console for errors |
| CORS error | Ensure flask-cors is installed |
| 404 errors | Verify API_BASE_URL in `script.js` |
| Slow loading | Reduce MAX_VIDEOS_TO_SCRAPE |

## 📈 Future Enhancements

- [ ] User authentication
- [ ] Favorites/Watchlist
- [ ] Category filtering
- [ ] Database integration
- [ ] Video quality selection
- [ ] Pagination
- [ ] Advanced search filters
- [ ] User comments
- [ ] Ratings system
- [ ] Recommendations

## 🤝 Contributing

This is a complete, working project. To modify:

1. **Frontend**: Edit HTML/CSS/JS files
2. **Backend**: Modify `app.py` or `scraper.py`
3. **Config**: Update `config.py`
4. **Test**: Run locally before deploying

## 📄 License

Educational project. Respect source website's terms of service.

---

**Built with ❤️ for educational purposes**
