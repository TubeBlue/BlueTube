# 🚀 Getting Started with Blue Tube

Welcome to Blue Tube! This guide will help you get up and running in minutes.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ **Python 3.8 or higher** installed
- ✅ **pip** (Python package manager)
- ✅ **Internet connection** (for scraping)
- ✅ **Modern web browser** (Chrome, Firefox, Edge, Safari)

### Check Python Installation

Open a terminal/command prompt and run:

```bash
python --version
```

You should see something like `Python 3.8.0` or higher.

---

## 🎯 Installation Steps

### Step 1: Open Terminal in Project Folder

Navigate to the Blue Tube project directory:

```bash
cd "d:/Website Project/WHentai/Blue Tube"
```

### Step 2: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Requests (HTTP library)
- BeautifulSoup4 (HTML parser)
- lxml (XML/HTML parser)

### Step 3: Verify Installation

Run the setup verification script:

```bash
python test_setup.py
```

This will check:
- ✓ Python version
- ✓ All dependencies installed
- ✓ All files present
- ✓ Scraper working
- ✓ Flask app ready

---

## 🎬 Running Blue Tube

### Option 1: Using Startup Scripts (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Start

```bash
python app.py
```

### Step 4: Access the Website

Once the server starts, open your browser and go to:

```
http://localhost:5000
```

Or simply open the `index.html` file directly in your browser (make sure the backend is running).

---

## 🎨 What You'll See

### First Time Launch

1. **Loading Screen**: You'll see a loading spinner
2. **Scraping**: Backend scrapes videos (takes a few seconds)
3. **Video Grid**: Videos appear in a Netflix-style grid
4. **Ready**: Browse, search, and watch videos!

### Main Interface

```
┌─────────────────────────────────────────────────────┐
│  BLUE TUBE    [Home] [Trending]    [Search] [↻]    │
├─────────────────────────────────────────────────────┤
│                                                      │
│              FEATURED CONTENT                        │
│      Discover premium entertainment                  │
│         [▶ Play] [ℹ More Info]                      │
│                                                      │
├─────────────────────────────────────────────────────┤
│  Trending Now                                       │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │
│  │Video │ │Video │ │Video │ │Video │              │
│  └──────┘ └──────┘ └──────┘ └──────┘              │
│                                                      │
│  Popular Videos                                     │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │
│  │Video │ │Video │ │Video │ │Video │              │
│  └──────┘ └──────┘ └──────┘ └──────┘              │
└─────────────────────────────────────────────────────┘
```

---

## 🎮 Using Blue Tube

### Browsing Videos

- **Scroll** through different sections (Trending, Popular, etc.)
- **Hover** over video cards to see the play button
- **Click** any video to open the player

### Searching

1. Click the **search box** in the top-right
2. Type your search query
3. Press **Enter** or click the search icon
4. Results appear instantly

### Playing Videos

1. **Click** a video card
2. **Modal opens** with video player
3. **Video plays** automatically
4. **Click X** or press **Escape** to close

### Refreshing Content

Click the **refresh button** (↻) in the navigation bar to fetch new videos.

---

## 🛠️ Configuration

### Change Port

Edit `app.py`:
```python
app.run(port=5000)  # Change to 8000, 3000, etc.
```

### Change Cache Duration

Edit `app.py`:
```python
CACHE_DURATION = timedelta(hours=1)  # Change to desired hours
```

### Change Number of Videos

Edit `app.py`:
```python
videos = scraper.scrape_homepage(max_videos=30)  # Change number
```

---

## 📱 Features Overview

### 🎬 Video Features
- **Grid Layout**: Netflix-style card display
- **Thumbnails**: Video preview images
- **Duration**: Video length displayed
- **Views**: View count shown
- **Play Button**: Hover effect

### 🔍 Search Features
- **Real-time**: Instant results
- **Title Search**: Search by video title
- **Clear Results**: Easy to read

### 🎨 UI Features
- **Responsive**: Works on all screen sizes
- **Dark Theme**: Easy on the eyes
- **Smooth Animations**: Professional feel
- **Loading States**: Clear feedback

### ⚡ Performance Features
- **Caching**: Fast repeated access
- **Background Scraping**: Non-blocking
- **Lazy Loading**: Images load as needed

---

## 🐛 Troubleshooting

### Problem: "No videos available"

**Solutions:**
1. Check that backend is running
2. Click the refresh button (↻)
3. Check backend console for errors
4. Wait a few seconds for initial scraping

### Problem: "Port already in use"

**Solutions:**
1. Close other applications using port 5000
2. Change port in `app.py`
3. Use `netstat -ano | findstr :5000` to find the process

### Problem: "Dependencies not installed"

**Solutions:**
1. Run `pip install -r requirements.txt`
2. Check Python version with `python --version`
3. Try `python -m pip install -r requirements.txt`

### Problem: "Videos not loading"

**Solutions:**
1. Check internet connection
2. Check backend console for errors
3. Try manual scraping: `python scraper.py`
4. Check if source website is accessible

### Problem: "CORS error"

**Solutions:**
1. Ensure `flask-cors` is installed
2. Check `API_BASE_URL` in `script.js`
3. Make sure backend is running

---

## 📊 API Testing

### Test API Status
```bash
curl http://localhost:5000/api/status
```

### Get All Videos
```bash
curl http://localhost:5000/api/videos
```

### Search Videos
```bash
curl http://localhost:5000/api/search?q=trending
```

### Force Refresh
```bash
curl http://localhost:5000/api/videos?refresh=true
```

---

## 🎓 Learning Resources

### Project Files to Explore

1. **index.html** - Learn HTML structure
2. **style.css** - Learn Netflix-style CSS
3. **script.js** - Learn JavaScript and APIs
4. **app.py** - Learn Flask and REST APIs
5. **scraper.py** - Learn web scraping

### Key Concepts

- **Frontend-Backend Communication**: How JavaScript talks to Python
- **Web Scraping**: Extracting data from websites
- **REST APIs**: Creating endpoints for data
- **Caching**: Improving performance
- **Responsive Design**: Mobile-friendly layouts

---

## 🚀 Next Steps

Once you're comfortable with the basics:

1. **Customize the UI**: Edit colors, fonts, layouts
2. **Add Features**: Implement favorites, categories
3. **Improve Scraping**: Add more data extraction
4. **Optimize Performance**: Database integration
5. **Deploy**: Put it online (Heroku, AWS, etc.)

---

## 📖 Additional Resources

- **README.md** - Full documentation
- **PROJECT_OVERVIEW.md** - Architecture details
- **QUICK_START.md** - Quick reference
- **config.py** - Configuration options

---

## 💡 Tips for Success

1. ✅ Always run `test_setup.py` after changes
2. ✅ Check browser console (F12) for errors
3. ✅ Check backend console for API errors
4. ✅ Use the refresh button to get new content
5. ✅ Keep the backend running while using the site

---

## 🎉 You're All Set!

Congratulations! You now have a fully functional Netflix-style video website with web scraping capabilities.

**Enjoy using Blue Tube!** 🎬

---

## 📞 Need Help?

1. Check the **Troubleshooting** section above
2. Review the **README.md** for detailed info
3. Run `python test_setup.py` to verify setup
4. Check console logs for error messages

---

**Happy Streaming! 🍿**
