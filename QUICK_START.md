# Blue Tube - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Or manually:**
```bash
python app.py
```

### Step 3: Open the Website
Open your browser and go to:
```
http://localhost:5000
```

Or open `index.html` directly in your browser (make sure the server is running).

---

## 🎯 Quick Commands

### Test the Scraper
```bash
python scraper.py
```
This will scrape videos and save them to `scraped_videos.json`.

### View API Status
Open in browser:
```
http://localhost:5000/api/status
```

### Force Refresh Videos
Click the refresh button (↻) in the top-right corner of the website.

---

## 📁 Project Files

- `index.html` - Main website page
- `style.css` - Netflix-style CSS
- `script.js` - Frontend JavaScript
- `app.py` - Flask backend server
- `scraper.py` - Web scraper
- `requirements.txt` - Python dependencies

---

## ⚙️ Configuration

### Change Port (in app.py)
```python
app.run(port=5000)  # Change 5000 to your desired port
```

### Change Cache Duration (in app.py)
```python
CACHE_DURATION = timedelta(hours=1)  # Change to desired duration
```

### Change Number of Videos (in app.py)
```python
videos = scraper.scrape_homepage(max_videos=30)  # Change 30 to desired number
```

---

## 🔧 Troubleshooting

### Port Already in Use
Change the port in `app.py` to a different number (e.g., 5001, 8000).

### Dependencies Not Installing
Make sure you have Python 3.8 or higher:
```bash
python --version
```

### No Videos Showing
1. Check that the backend is running
2. Check browser console (F12) for errors
3. Try clicking the refresh button
4. Check backend console for scraping errors

---

## 🎨 Features

✅ Netflix-inspired modern UI  
✅ Video search functionality  
✅ Responsive design (mobile-friendly)  
✅ Auto-caching for performance  
✅ Video embedding with iframe  
✅ Background scraping  
✅ Real-time search  

---

## 📝 Notes

- Videos are cached for 1 hour by default
- The scraper respects rate limits
- First load may take a few seconds while scraping
- Use the refresh button to get fresh content

---

## 🌐 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/videos` | Get all videos |
| `/api/videos?refresh=true` | Force refresh |
| `/api/videos/<id>` | Get specific video |
| `/api/search?q=query` | Search videos |
| `/api/status` | Server status |
| `/api/scrape` | Trigger scraping |

---

**Enjoy your Blue Tube experience! 🎬**
