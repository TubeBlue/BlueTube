// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State Management
let allVideos = [];
let filteredVideos = [];
let currentPage = 1;
let videosPerPage = 20;
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
    initApp();
    setupEventListeners();
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

// Initialize Application
async function initApp() {
    await loadVideos();
}

// Load Videos from API
async function loadVideos(forceRefresh = false) {
    try {
        showLoading(true);
        
        const endpoint = forceRefresh ? '/videos?refresh=true' : '/videos';
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success && data.videos) {
            allVideos = data.videos;
            filteredVideos = [...allVideos];
            displayVideos(filteredVideos);
        } else {
            throw new Error(data.error || 'Failed to load videos');
        }
        
        showLoading(false);
    } catch (error) {
        console.error('Error loading videos:', error);
        showError(error.message);
        showLoading(false);
    }
}

// Display Videos
function displayVideos(videos) {
    videoContainer.innerHTML = '';
    
    if (!videos || videos.length === 0) {
        showEmptyState();
        return;
    }

    // Group videos by category (for demo, we'll create sections)
    const sections = [
        { title: 'Trending Now', videos: videos.slice(0, Math.min(8, videos.length)) },
        { title: 'Popular Videos', videos: videos.slice(8, Math.min(16, videos.length)) },
        { title: 'Recently Added', videos: videos.slice(16) }
    ].filter(section => section.videos.length > 0);

    sections.forEach(section => {
        const rowElement = createVideoRow(section.title, section.videos);
        videoContainer.appendChild(rowElement);
    });
}

// Create Video Row
function createVideoRow(title, videos) {
    const row = document.createElement('div');
    row.className = 'video-row';
    
    const rowTitle = document.createElement('h2');
    rowTitle.className = 'row-title';
    rowTitle.textContent = title;
    
    const grid = document.createElement('div');
    grid.className = 'video-grid';
    
    videos.forEach(video => {
        const card = createVideoCard(video);
        grid.appendChild(card);
    });
    
    row.appendChild(rowTitle);
    row.appendChild(grid);
    
    return row;
}

// Create Video Card
function createVideoCard(video) {
    const card = document.createElement('div');
    card.className = 'video-card';
    card.setAttribute('data-video-id', video.id || video.video_url || '');
    
    // Thumbnail
    const thumbnail = document.createElement('div');
    thumbnail.className = 'video-thumbnail';
    
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
    thumbnail.appendChild(watchLaterBtn);
    
    // Play Icon
    const playIcon = document.createElement('div');
    playIcon.className = 'play-icon';
    playIcon.innerHTML = '▶';
    thumbnail.appendChild(playIcon);
    
    // Video Info
    const info = document.createElement('div');
    info.className = 'video-info';
    
    const title = document.createElement('h3');
    title.className = 'video-title';
    title.textContent = video.title || 'Untitled Video';
    title.title = video.title || 'Untitled Video'; // Show full title on hover
    
    const meta = document.createElement('div');
    meta.className = 'video-meta';
    
    const duration = document.createElement('span');
    duration.className = 'video-duration';
    duration.textContent = video.duration || 'N/A';
    
    const views = document.createElement('span');
    views.className = 'video-views';
    views.textContent = video.views || '';
    
    meta.appendChild(duration);
    if (video.views) {
        meta.appendChild(views);
    }
    
    info.appendChild(title);
    info.appendChild(meta);
    
    card.appendChild(thumbnail);
    card.appendChild(info);
    
    // Click event to open modal
    card.addEventListener('click', () => openModal(video));
    
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
    } else {
        // Add to watch later
        watchLaterList.push(video);
        button.innerHTML = '✓';
        button.classList.add('added');
        button.title = 'Added to Watch Later';
    }
    
    localStorage.setItem('watchLater', JSON.stringify(watchLaterList));
}

// Open Video Modal
function openModal(video) {
    if (!video) return;
    
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
                <h3 style="color:white;margin-bottom:20px;font-size:24px;">Watch Video</h3>
                <button onclick="window.open('${video.video_url}', '_blank')" style="padding:15px 40px;background:white;color:#2962ff;border:none;border-radius:8px;font-size:18px;font-weight:600;cursor:pointer;transition:all 0.3s ease;">
                    Open Video in New Tab
                </button>
                <p style="color:rgba(255,255,255,0.7);margin-top:15px;font-size:14px;">Click to watch on the original site</p>
            </div>
        `;
    } else {
        modalVideo.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#999;">Video not available</div>';
    }
    
    // Set video info
    modalTitle.textContent = video.title || 'Untitled Video';
    modalDuration.textContent = video.duration || 'N/A';
    modalViews.textContent = video.views || 'No views data';
    modalDescription.textContent = video.description || 'No description available.';
    
    // Show modal
    videoModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close Video Modal
function closeModal() {
    videoModal.classList.remove('active');
    modalVideo.innerHTML = '';
    document.body.style.overflow = 'auto';
}

// Handle Search
function handleSearch() {
    const query = searchInput.value.trim().toLowerCase();
    
    if (!query) {
        filteredVideos = [...allVideos];
    } else {
        filteredVideos = allVideos.filter(video => 
            video.title?.toLowerCase().includes(query)
        );
    }
    
    displayVideos(filteredVideos);
}

// Show Loading State
function showLoading(show) {
    if (show) {
        loadingSpinner.style.display = 'flex';
        videoContainer.style.display = 'none';
    } else {
        loadingSpinner.style.display = 'none';
        videoContainer.style.display = 'block';
    }
}

// Show Error State
function showError(message) {
    videoContainer.innerHTML = `
        <div class="error-message">
            <h3>Oops! Something went wrong</h3>
            <p>${message}</p>
            <p>Please make sure the backend server is running on port 5000</p>
            <button onclick="location.reload()">Try Again</button>
        </div>
    `;
}

// Show Empty State
function showEmptyState() {
    videoContainer.innerHTML = `
        <div class="error-message">
            <h3>No Videos Found</h3>
            <p>Try a different search term or refresh the page</p>
            <button onclick="location.reload()">Refresh</button>
        </div>
    `;
}

// Utility: Format Duration
function formatDuration(seconds) {
    if (!seconds) return 'N/A';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

// Utility: Format Views
function formatViews(views) {
    if (!views) return '';
    
    const num = parseInt(views);
    if (isNaN(num)) return views;
    
    if (num >= 1000000) {
        return `${(num / 1000000).toFixed(1)}M views`;
    } else if (num >= 1000) {
        return `${(num / 1000).toFixed(1)}K views`;
    }
    return `${num} views`;
}
