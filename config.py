"""
Blue Tube - Configuration File
Edit these settings to customize the application
"""

# Server Configuration
SERVER_HOST = '0.0.0.0'  # Use '0.0.0.0' to allow external access, '127.0.0.1' for local only
SERVER_PORT = 5000       # Port to run the server on
DEBUG_MODE = True        # Set to False in production

# Scraper Configuration
MAX_VIDEOS_TO_SCRAPE = 30           # Maximum number of videos to scrape per request
SCRAPER_TIMEOUT = 10                # Timeout for HTTP requests in seconds
SCRAPER_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Cache Configuration
CACHE_DURATION_HOURS = 1            # How long to cache videos (in hours)
CACHE_FILE = 'video_cache.json'     # File to store cached videos

# API Configuration
ENABLE_CORS = True                  # Enable Cross-Origin Resource Sharing
API_PREFIX = '/api'                 # API endpoint prefix

# Frontend Configuration
VIDEOS_PER_SECTION = 8              # Number of videos to show per section

# Rate Limiting (for scraper)
REQUEST_DELAY = 1                   # Seconds to wait between requests (be respectful)
MAX_RETRIES = 3                     # Maximum number of retry attempts

# Feature Flags
ENABLE_SEARCH = True                # Enable search functionality
ENABLE_BACKGROUND_SCRAPING = True   # Enable background scraping
ENABLE_AUTO_REFRESH = True          # Auto-refresh expired cache

# Logging
LOG_LEVEL = 'INFO'                  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = 'blue_tube.log'          # Log file name (None to disable file logging)

# Security (for production)
SECRET_KEY = 'change-this-in-production'  # Change this for production use
ALLOWED_ORIGINS = ['*']             # CORS allowed origins (* = all, or list specific domains)

# Performance
ENABLE_COMPRESSION = True           # Enable gzip compression
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max upload size (16 MB)

# Database (for future use)
USE_DATABASE = False                # Enable database storage instead of JSON cache
DATABASE_URL = 'sqlite:///videos.db'  # Database connection string
