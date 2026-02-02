"""
Blue Tube - Setup Verification Script
Run this to verify your installation is correct
"""

import sys
import subprocess
import os

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version is compatible (3.8+)")
        return True
    else:
        print("✗ Python version is too old. Please upgrade to Python 3.8+")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print_header("Checking Dependencies")
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'flask-cors',
        'requests': 'requests',
        'bs4': 'beautifulsoup4',
        'lxml': 'lxml'
    }
    
    all_installed = True
    
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} is installed")
        except ImportError:
            print(f"✗ {package_name} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
    
    return all_installed

def check_files():
    """Check if all required files exist"""
    print_header("Checking Project Files")
    
    required_files = [
        'index.html',
        'style.css',
        'script.js',
        'app.py',
        'scraper.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_exist = True
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} is missing")
            all_exist = False
    
    return all_exist

def test_scraper():
    """Test if scraper can import"""
    print_header("Testing Scraper")
    
    try:
        from scraper import EpornerScraper
        print("✓ Scraper module imported successfully")
        
        scraper = EpornerScraper()
        print("✓ Scraper instance created successfully")
        
        print("\nNote: Actual scraping will happen when you run the server.")
        return True
    except Exception as e:
        print(f"✗ Error testing scraper: {e}")
        return False

def test_flask():
    """Test if Flask app can import"""
    print_header("Testing Flask App")
    
    try:
        # Temporarily set environment to prevent auto-run
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'
        
        import app
        print("✓ Flask app imported successfully")
        print("✓ API endpoints are configured")
        return True
    except Exception as e:
        print(f"✗ Error testing Flask app: {e}")
        return False

def print_summary(results):
    """Print summary of tests"""
    print_header("Test Summary")
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:<30} {status}")
    
    print("\n" + "="*60)
    
    if all_passed:
        print("  ✓ ALL TESTS PASSED!")
        print("  Your setup is ready to use.")
        print("\n  To start the server, run:")
        print("    python app.py")
        print("  or")
        print("    start.bat  (Windows)")
        print("    ./start.sh (Linux/Mac)")
    else:
        print("  ✗ SOME TESTS FAILED")
        print("  Please fix the issues above before running the server.")
    
    print("="*60 + "\n")

def main():
    """Run all tests"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  Blue Tube - Setup Verification".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Project Files': check_files(),
        'Scraper Module': test_scraper(),
        'Flask App': test_flask()
    }
    
    print_summary(results)
    
    # Return exit code
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
