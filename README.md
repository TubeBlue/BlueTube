# Blue Tube

A modern Netflix-style video streaming website with a Python web scraper backend.

## Features

- 🎬 **Netflix-like UI**: Clean, modern interface inspired by Netflix
- 🔍 **Search Functionality**: Search through video content
- 🔄 **Auto-refresh**: Automatic content updates with caching
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🎥 **Video Embedding**: Direct video playback with iframe embedding
- ⚡ **Fast Loading**: Smart caching system for improved performance

## Project Structure

```
Blue Tube/
├── index.html          # Main frontend HTML file
├── style.css           # CSS styling (Netflix-inspired)
├── script.js           # Frontend JavaScript logic
├── app.py              # Flask backend API server
├── scraper.py          # Web scraper for eporner.com
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Installation

Check that all packages are installed:

```bash
pip list
```

You should see Flask, flask-cors, requests, beautifulsoup4, and lxml in the list.

## Usage

### Starting the Backend Server

1. Open a terminal in the project directory
2. Run the Flask server:

```bash
python app.py
```

3. The server will start on `http://localhost:5000`
4. You should see:
   ```
   ==================================================
   Blue Tube API Server
   ==================================================
   API Server is ready!
   Frontend URL: http://localhost:5000
   API URL: http://localhost:5000/api
   ==================================================
   ```

### Accessing the Website

1. Open your web browser
2. Navigate to `http://localhost:5000` or open `index.html` directly
3. The website will automatically fetch videos from the backend
4. If opening `index.html` directly, make sure the backend server is running

### Testing the Scraper

To test the scraper independently:

```bash
python scraper.py
```

This will scrape videos and save them to `scraped_videos.json`.

## API Endpoints

### GET /api/videos
Get all cached videos

**Parameters:**
- `refresh` (optional): Set to `true` to force refresh from source

**Example:**
```
http://localhost:5000/api/videos
http://localhost:5000/api/videos?refresh=true
```

### GET /api/videos/<video_id>
Get a specific video by ID

**Example:**
```
http://localhost:5000/api/videos/video_1
```

### GET /api/search?q=<query>
Search for videos

**Parameters:**
- `q`: Search query

**Example:**
```
http://localhost:5000/api/search?q=trending
```

### GET /api/status
Get API server status

**Example:**
```
http://localhost:5000/api/status
```

### GET /api/scrape
Manually trigger video scraping

**Example:**
```
http://localhost:5000/api/scrape
```

## Configuration

### Cache Duration
Videos are cached for 1 hour by default. To change this, edit `app.py`:

```python
CACHE_DURATION = timedelta(hours=1)  # Change to desired duration
```

### Maximum Videos
To change the number of videos scraped, edit `app.py`:

```python
videos = scraper.scrape_homepage(max_videos=30)  # Change 30 to desired number
```

### API Base URL
If running on a different port or host, update `script.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';  // Change as needed
```

## Features Explained

### Caching System
- Videos are cached to reduce server load and improve performance
- Cache is automatically refreshed after 1 hour
- Manual refresh available via the refresh button in the UI

### Video Embedding
- The scraper extracts video information and generates embed URLs
- Videos are displayed using iframe embedding
- Click any video card to open the video player modal

### Responsive Design
- Mobile-first design approach
- Adapts to different screen sizes
- Touch-friendly interface

### Search Functionality
- Real-time search through video titles
- Searches both cached and live content
- Instant results display

## Troubleshooting

### "No videos available" Error
- Check that the backend server is running
- Try clicking the refresh button (↻) in the navigation bar
- Check the console for error messages

### Backend Server Won't Start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is already in use
- Try running on a different port: `app.run(port=5001)`

### Videos Not Loading
- Verify internet connection
- Check if the source website is accessible
- Look at backend console for scraping errors

### CORS Errors
- Make sure flask-cors is installed
- Check that the API URL in `script.js` matches the backend URL

## Development

### Adding New Features

1. **Frontend**: Edit `index.html`, `style.css`, or `script.js`
2. **Backend**: Edit `app.py` for API changes
3. **Scraper**: Edit `scraper.py` for scraping logic changes

### Debugging

Enable debug mode in `app.py`:
```python
app.run(debug=True)
```

Check browser console (F12) for frontend errors.

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+
- ✅ Opera 76+

## Performance Tips

1. **Reduce Cache Duration**: For more frequent updates, reduce `CACHE_DURATION`
2. **Limit Videos**: Scrape fewer videos for faster loading
3. **Use CDN**: Host static files on a CDN for better performance
4. **Enable Gzip**: Enable compression in production

## Security Notes

- The scraper respects robots.txt and site terms
- Uses appropriate user agents
- Implements rate limiting to avoid overwhelming servers
- CORS is enabled for development (configure for production)

## License

This project is for educational purposes. Ensure you have proper permissions before scraping any website.

## Credits

- UI Design: Inspired by Netflix
- Icons: SVG icons
- Framework: Flask (Python)
- Frontend: Vanilla JavaScript

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the console logs
3. Verify all dependencies are installed
4. Ensure the backend server is running

---

**Note**: This application is designed for educational purposes. Always respect website terms of service and robots.txt when scraping content.
