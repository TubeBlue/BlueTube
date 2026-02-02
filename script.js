// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State Management
let allVideos = [];
let filteredVideos = [];
let currentPage = 1;
let videosPerPage = 36; // Display 36 videos per page
let totalPages = 1;
let currentSearchQuery = '';
let watchLaterList = JSON.parse(localStorage.getItem('watchLater') || '[]');

// DOM Elements
const videoContainer = document.getElementById('videoContainer');
const loadingSpinner = document.getElementById('loadingSpinner');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const refreshBtn = document.getElementById('refreshBtn');
const videoModal = document.getElementById('videoModal');
const modalOverlay = document.getElementById('modalOverlay');
const modalClose = document.getElementById('modalClose');
const modalVideo = document.getElementById('modalVideo');
const modalTitle = document.getElementById('modalTitle');
const modalDuration = document.getElementById('modalDuration');
const modalViews = document.getElementById('modalViews');
const modalDescription = document.getElementById('modalDescription');
const navbar = document.querySelector('.navbar');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    // Check age verification and load content
    checkAgeVerificationAndLoad();
});

// Setup Event Listeners
function setupEventListeners() {
    // Search functionality
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });

    // Refresh button
    refreshBtn.addEventListener('click', () => {
        currentPage = 1;
        loadVideos(true);
    });

    // Modal close
    modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', closeModal);

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Close modal on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && videoModal.classList.contains('active')) {
            closeModal();
        }
    });
}

// Check age verification and load content
function checkAgeVerificationAndLoad() {
    const ageVerified = localStorage.getItem('ageVerified');
    const ageModal = document.getElementById('ageVerificationModal');
    
    if (!ageVerified) {
        // Show age verification modal
        if (ageModal) {
            ageModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            
            // Setup button handlers
            document.getElementById('ageYesBtn').addEventListener('click', function() {
                localStorage.setItem('ageVerified', 'true');
                ageModal.style.display = 'none';
                document.body.style.overflow = 'auto';
                // Load content
                loadVideos();
            });
            
            document.getElementById('ageNoBtn').addEventListener('click', function() {
                // Redirect under-18 users
                window.location.href = 'https://www.youtube.com/watch?v=qQ6ipvQbgpc';
            });
        }
    } else {
        // Hide age modal if already verified and load content
        if (ageModal) {
            ageModal.style.display = 'none';
        }
        loadVideos();
    }
}

// Load Videos from API with Pagination
async function loadVideos(refresh = false) {
    try {
        loadingSpinner.style.display = 'flex';
        if (videoContainer) {
            videoContainer.innerHTML = '';
        }
        currentSearchQuery = '';
        
        const url = refresh ? 
            `${API_BASE_URL}/videos?refresh=true&page=${currentPage}&per_page=${videosPerPage}` : 
            `${API_BASE_URL}/videos?page=${currentPage}&per_page=${videosPerPage}`;
            
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Failed to load videos');
        }
        
        const data = await response.json();
        
        if (data.success && data.videos) {
            allVideos = data.videos;
            filteredVideos = allVideos;
            totalPages = data.total_pages || Math.ceil(data.total / videosPerPage) || 1;
            displayVideosWithPagination(allVideos);
        } else if (data.is_scraping) {
            // Show scraping message
            if (videoContainer) {
                videoContainer.innerHTML = `
                    <div class="loading-container">
                        <div class="loading-spinner"></div>
                        <p>${data.message || 'Scraping videos from multiple sources...'}</p>
                        <p>This may take a minute on first load...</p>
                        <button onclick="loadVideos()" style="margin-top: 20px; background: var(--netflix-red); color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;">Refresh</button>
                    </div>
                `;
            }
        } else {
            showError('No videos available');
        }
    } catch (error) {
        console.error('Error loading videos:', error);
        showError('Failed to load videos. Please try again.');
    } finally {
        if (loadingSpinner) {
            loadingSpinner.style.display = 'none';
        }
    }
}

// Search Videos
async function searchVideos(query) {
    try {
        if (loadingSpinner) {
            loadingSpinner.style.display = 'flex';
        }
        if (videoContainer) {
            videoContainer.innerHTML = '';
        }
        
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Search failed');
        }
        
        const data = await response.json();
        
        if (data.success && data.videos && data.videos.length > 0) {
            filteredVideos = data.videos;
            displaySearchResults(filteredVideos, query);
        } else {
            showSearchNoResults(query);
        }
    } catch (error) {
        console.error('Error searching videos:', error);
        showError('Search failed. Please try again.');
    } finally {
        if (loadingSpinner) {
            loadingSpinner.style.display = 'none';
        }
    }
}

// Perform Search
function performSearch() {
    const query = searchInput.value.trim();
    if (query) {
        currentSearchQuery = query;
        currentPage = 1;
        if (window.history) {
            window.history.pushState({}, '', `?search=${encodeURIComponent(query)}`);
        }
        searchVideos(query);
    }
}

// Display Search Results
function displaySearchResults(videos, query) {
    if (!videoContainer) return;
    
    videoContainer.innerHTML = '';
    
    // Search header
    const header = document.createElement('div');
    header.className = 'search-results-header';
    header.innerHTML = `
        <h2>Search Results for "${query}" (${videos.length} videos)</h2>
        <button class="clear-search" onclick="clearSearch()" style="background: var(--netflix-red); color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Clear Search</button>
    `;
    videoContainer.appendChild(header);
    
    // Display videos
    if (videos.length > 0) {
        const section = document.createElement('div');
        section.className = 'section';
        
        const grid = document.createElement('div');
        grid.className = 'video-row';
        
        videos.forEach(video => {
            const card = createVideoCard(video);
            grid.appendChild(card);
        });
        
        section.appendChild(grid);
        videoContainer.appendChild(section);
    }
}

// Show No Search Results
function showSearchNoResults(query) {
    if (!videoContainer) return;
    
    videoContainer.innerHTML = `
        <div class="search-results-header">
            <h2>No results for "${query}"</h2>
            <button class="clear-search" onclick="clearSearch()" style="background: var(--netflix-red); color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Clear Search</button>
        </div>
        <div class="no-videos">
            <p>No videos found matching your search. Try different keywords.</p>
        </div>
    `;
}

// Clear Search
function clearSearch() {
    if (searchInput) {
        searchInput.value = '';
    }
    currentSearchQuery = '';
    currentPage = 1;
    if (window.history) {
        window.history.pushState({}, '', window.location.pathname);
    }
    loadVideos();
}

// Display Videos with Pagination
function displayVideosWithPagination(videos) {
    if (!videoContainer) return;
    
    videoContainer.innerHTML = '';
    
    if (videos.length === 0) {
        showError('No videos to display');
        return;
    }
    
    // Create sections for better organization
    const section = document.createElement('div');
    section.className = 'section';
    
    const titleDiv = document.createElement('div');
    titleDiv.className = 'section-title';
    titleDiv.innerHTML = `
        <span>All Videos (Page ${currentPage} of ${totalPages})</span>
    `;
    section.appendChild(titleDiv);
    
    const grid = document.createElement('div');
    grid.className = 'video-row';
    
    videos.forEach(video => {
        const card = createVideoCard(video);
        grid.appendChild(card);
    });
    
    section.appendChild(grid);
    videoContainer.appendChild(section);
    
    // Add pagination controls
    addPaginationControls();
}

// Add Pagination Controls
function addPaginationControls() {
    if (!videoContainer) return;
    
    const paginationDiv = document.createElement('div');
    paginationDiv.className = 'pagination';
    paginationDiv.style.cssText = 'display: flex; justify-content: center; align-items: center; gap: 20px; margin: 30px 0; padding: 20px;';
    
    // Previous button
    const prevBtn = document.createElement('button');
    prevBtn.textContent = '← Previous';
    prevBtn.disabled = currentPage === 1;
    prevBtn.onclick = () => changePage(currentPage - 1);
    prevBtn.style.cssText = 'background: var(--netflix-red); color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;';
    if (prevBtn.disabled) {
        prevBtn.style.opacity = '0.5';
        prevBtn.style.cursor = 'not-allowed';
    }
    paginationDiv.appendChild(prevBtn);
    
    // Page info
    const pageInfo = document.createElement('span');
    pageInfo.className = 'page-info';
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    pageInfo.style.cssText = 'color: var(--text-primary); font-size: 16px;';
    paginationDiv.appendChild(pageInfo);
    
    // Next button
    const nextBtn = document.createElement('button');
    nextBtn.textContent = 'Next →';
    nextBtn.disabled = currentPage >= totalPages;
    nextBtn.onclick = () => changePage(currentPage + 1);
    nextBtn.style.cssText = 'background: var(--netflix-red); color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;';
    if (nextBtn.disabled) {
        nextBtn.style.opacity = '0.5';
        nextBtn.style.cursor = 'not-allowed';
    }
    paginationDiv.appendChild(nextBtn);
    
    videoContainer.appendChild(paginationDiv);
}

// Change Page
async function changePage(page) {
    if (page < 1 || page > totalPages) return;
    
    currentPage = page;
    if (window) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    if (currentSearchQuery) {
        await searchVideos(currentSearchQuery);
    } else {
        await loadVideos();
    }
}

// Create Video Card
function createVideoCard(video) {
    const card = document.createElement('div');
    card.className = 'video-card';
    card.setAttribute('data-video-id', video.id || video.video_url || '');
    
    // Thumbnail
    const thumbnail = document.createElement('div');
    thumbnail.className = 'video-thumbnail';
    thumbnail.style.cssText = 'width: 100%; aspect-ratio: 16/9; background: linear-gradient(135deg, rgba(20, 20, 20, 0.9), rgba(30, 30, 30, 0.9)); background-size: cover; background-position: center; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden;';
    
    if (video.thumbnail && video.thumbnail.trim() !== '') {
        thumbnail.style.backgroundImage = `url('${video.thumbnail}')`;
        thumbnail.style.backgroundSize = 'cover';
        thumbnail.style.backgroundPosition = 'center';
        thumbnail.style.backgroundRepeat = 'no-repeat';
    }
    
    // Watch Later Button
    const watchLaterBtn = document.createElement('button');
    watchLaterBtn.className = 'watch-later-btn';
    const isInWatchLater = watchLaterList.some(v => (v.video_url || v.id) === (video.video_url || video.id));
    watchLaterBtn.innerHTML = isInWatchLater ? '✓' : '+';
    if (isInWatchLater) {
        watchLaterBtn.classList.add('added');
    }
    watchLaterBtn.title = isInWatchLater ? 'Added to Watch Later' : 'Add to Watch Later';
    watchLaterBtn.onclick = (e) => {
        e.stopPropagation();
        toggleWatchLater(video, watchLaterBtn);
    };
    watchLaterBtn.style.cssText = 'position: absolute; top: 10px; right: 10px; background: rgba(0, 0, 0, 0.7); color: white; width: 30px; height: 30px; border-radius: 50%; border: none; font-size: 18px; cursor: pointer; z-index: 2;';
    thumbnail.appendChild(watchLaterBtn);
    
    // Play Icon
    const playIcon = document.createElement('div');
    playIcon.className = 'play-icon';
    playIcon.innerHTML = '▶';
    playIcon.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 50px; height: 50px; background: rgba(229, 9, 20, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; color: white; opacity: 0; transition: opacity 0.3s ease; z-index: 2;';
    thumbnail.appendChild(playIcon);
    
    // Video Info
    const info = document.createElement('div');
    info.className = 'video-info';
    info.style.cssText = 'padding: 15px; background: linear-gradient(to bottom, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 1));';
    
    const title = document.createElement('h3');
    title.className = 'video-title';
    title.textContent = video.title || 'Untitled Video';
    title.title = video.title || 'Untitled Video';
    title.style.cssText = 'font-size: 15px; font-weight: 600; margin-bottom: 8px; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; line-height: 1.4; color: var(--text-primary);';
    
    const meta = document.createElement('div');
    meta.className = 'video-meta';
    meta.style.cssText = 'display: flex; gap: 12px; align-items: center; flex-wrap: wrap; font-size: 13px;';
    
    const duration = document.createElement('span');
    duration.className = 'video-duration';
    duration.textContent = video.duration || 'N/A';
    duration.style.cssText = 'background: rgba(229, 9, 20, 0.9); padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 12px;';
    
    const views = document.createElement('span');
    views.className = 'video-views';
    views.textContent = video.views || 'N/A';
    views.style.cssText = 'color: var(--text-secondary); font-size: 13px;';
    
    meta.appendChild(duration);
    meta.appendChild(views);
    
    info.appendChild(title);
    info.appendChild(meta);
    
    card.appendChild(thumbnail);
    card.appendChild(info);
    
    // Click event to open modal
    card.addEventListener('click', () => openModal(video));
    
    // Add hover effect
    card.addEventListener('mouseenter', () => {
        playIcon.style.opacity = '1';
    });
    
    card.addEventListener('mouseleave', () => {
        playIcon.style.opacity = '0';
    });
    
    return card;
}

// Toggle Watch Later
function toggleWatchLater(video, button) {
    const videoId = video.video_url || video.id;
    const index = watchLaterList.findIndex(v => (v.video_url || v.id) === videoId);
    
    if (index > -1) {
        // Remove from watch later
        watchLaterList.splice(index, 1);
        button.innerHTML = '+';
        button.classList.remove('added');
        button.title = 'Add to Watch Later';
        showNotification('Removed from Watch Later');
    } else {
        // Add to watch later
        watchLaterList.push(video);
        button.innerHTML = '✓';
        button.classList.add('added');
        button.title = 'Added to Watch Later';
        showNotification('Added to Watch Later');
    }
    
    localStorage.setItem('watchLater', JSON.stringify(watchLaterList));
}

// Show Notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: var(--netflix-red);
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 2000);
}

// Open Video Modal
function openModal(video) {
    if (!video || !videoModal || !modalVideo) return;
    
    console.log('Opening video modal with data:', video);
    
    // Use proper embed URL with iframe
    if (video.embed_url) {
        modalVideo.innerHTML = `<iframe src="${video.embed_url}" width="100%" height="100%" frameborder="0" allowfullscreen allow="autoplay"></iframe>`;
    } else if (video.video_url) {
        // Fallback: open in new tab if no embed URL
        modalVideo.innerHTML = `
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;background:linear-gradient(135deg, #1a237e 0%, #2962ff 100%);">
                <svg width="80" height="80" viewBox="0 0 24 24" fill="white" style="margin-bottom:20px;">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
                <p style="color:white;font-size:18px;">Video player not available</p>
                <button onclick="window.open('${video.video_url}', '_blank')" style="margin-top:20px;padding:12px 30px;background:#e50914;color:white;border:none;border-radius:6px;cursor:pointer;font-size:16px;">Watch on Source Website</button>
            </div>
        `;
    } else {
        modalVideo.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#999;">Video not available</div>';
    }
    
    // Display video information
    if (modalTitle) {
        modalTitle.textContent = video.title || 'Untitled Video';
    }
    if (modalDuration) {
        modalDuration.textContent = `⏱️ ${video.duration || 'N/A'}`;
    }
    if (modalViews) {
        modalViews.textContent = `👁️ ${video.views || 'No views data'}`;
    }
    
    // Display description with fallback
    let description = video.description || video.title || 'No description available.';
    if (video.tags && video.tags.length > 0) {
        description += `\n\nTags: ${Array.isArray(video.tags) ? video.tags.join(', ') : video.tags}`;
    }
    if (video.source) {
        description += `\n\nSource: ${video.source}`;
    }
    if (modalDescription) {
        modalDescription.textContent = description;
    }
    
    videoModal.classList.add('active');
    if (document.body) {
        document.body.style.overflow = 'hidden';
    }
}

// Close Modal
function closeModal() {
    if (videoModal) {
        videoModal.classList.remove('active');
    }
    if (modalVideo) {
        modalVideo.innerHTML = '';
    }
    if (document.body) {
        document.body.style.overflow = 'auto';
    }
}

// Show Error
function showError(message) {
    if (!videoContainer) return;
    
    videoContainer.innerHTML = `
        <div class="error-message" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px; text-align: center; padding: 20px;">
            <h3 style="font-size: 24px; margin-bottom: 15px;">Oops!</h3>
            <p style="font-size: 18px; margin-bottom: 20px; color: var(--text-secondary);">${message}</p>
            <button onclick="location.reload()" style="background: var(--netflix-red); color: white; border: none; padding: 12px 30px; border-radius: 6px; cursor: pointer; font-size: 16px;">Retry</button>
        </div>
    `;
}

// Show Loading Message
function showLoadingMessage(message) {
    if (!videoContainer) return;
    
    videoContainer.innerHTML = `
        <div class="loading-container" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 100px 0;">
            <div class="loading-spinner" style="width: 50px; height: 50px; border: 4px solid rgba(255, 255, 255, 0.1); border-top-color: var(--netflix-red); border-radius: 50%; animation: spin 1s cubic-bezier(0.5, 0, 0.5, 1) infinite;"></div>
            <p style="margin-top: 20px; color: var(--text-secondary); font-size: 16px; text-align: center;">${message}</p>
        </div>
    `;
}

// Make clearSearch available globally
window.clearSearch = clearSearch;