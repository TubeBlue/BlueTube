@echo off
echo ========================================
echo   Blue Tube - Massive Video Scraper
echo ========================================
echo.
echo This will scrape thousands of videos from 8 sources.
echo.
echo Recommended options:
echo   100   = ~800 videos (Quick test)
echo   1000  = ~8,000 videos (1 hour)
echo   5000  = ~40,000 videos (4 hours)
echo   10000 = ~80,000 videos (8 hours)
echo   15000 = ~120,000 videos (12 hours)
echo.
echo ========================================
echo.

python enhanced_scraper.py

echo.
echo ========================================
echo   Scraping Complete!
echo ========================================
echo.
echo Next step: Run start.bat to launch the server
echo.
pause
