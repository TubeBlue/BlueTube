// Trending Page JavaScript
const API_BASE_URL = 'http://localhost:5000/api';

// State
let currentPage = 1;
let totalPages = 1;
let isLoading = false;

// DOM Elements
const trendingVideos = document.getElementById('trendingVideos');
const loadingState = document.getElementById('loadingState');
const noVideos = document.getElementById('noVideos');
const videoModal = document.getElementById('videoModal');
const modalVideo = document.getElementById('modalVideo');
const modalTitle = document.getElementById('modalTitle');
const modalDuration = document.getElementById('modalDuration');
const modalViews = document.getElementById('modalViews');
const modalDescription = document.getElementById('modalDescription');
const addToListBtn = document.getElementById('addToListBtn');

let currentVideo = null;

// Load Trending Videos
async function loadTrendingVideos(append = false) {
    if (isLoading) return;
    
    try {
        isLoading = true;
        
        if (!append) {
            loadingState.style.display = 'flex';
            trendingVideos.innerHTML = '';
            currentPage = 1;
        }
        
        noVideos.style.display = 'none';

        const response = await fetch(`${API_BASE_URL}/trending?page=${currentPage}&per_page=200`);
        const data = await response.json();

        loadingState.style.display = 'none';
        isLoading = false;

        if (data.success && data.videos && data.videos.length > 0) {
            totalPages = data.total_pages || 1;
            displayVideos(data.videos, append);
            
            // Add pagination info
            updatePaginationInfo(data);
        } else {
            noVideos.style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading trending videos:', error);
        loadingState.style.display = 'none';
        isLoading = false;
        noVideos.style.display = 'block';
        noVideos.innerHTML = '<p style="color: #e50914;">Failed to load trending videos. Please try again.</p>';
    }
}

// Update pagination info
function updatePaginationInfo(data) {
    let paginationDiv = document.getElementById('paginationInfo');
    
    if (!paginationDiv) {
        paginationDiv = document.createElement('div');
        paginationDiv.id = 'paginationInfo';
        paginationDiv.style.cssText = 'text-align: center; margin: 30px 0; padding: 20px;';
        document.querySelector('.section').appendChild(paginationDiv);
    }
    
    paginationDiv.innerHTML = `
        <p style="color: #ccc; margin-bottom: 20px;">
            Showing ${data.videos.length} of ${data.total} trending videos (Page ${data.page} of ${data.total_pages})
        </p>
        <div style="display: flex; justify-content: center; gap: 10px;">
            ${data.page > 1 ? '<button onclick="previousPage()" class="btn-pagination">← Previous</button>' : ''}
            ${data.page < data.total_pages ? '<button onclick="nextPage()" class="btn-pagination">Next →</button>' : ''}
        </div>
    `;
}

// Pagination functions
function nextPage() {
    if (currentPage < totalPages) {
        currentPage++;
        loadTrendingVideos(false);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        loadTrendingVideos(false);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Display Videos
function displayVideos(videos) {
    trendingVideos.innerHTML = '';
    
    videos.forEach((video, index) => {
        const videoCard = createVideoCard(video, index + 1);
        trendingVideos.appendChild(videoCard);
    });
}

// Create Video Card with Rank
function createVideoCard(video, rank) {
    const card = document.createElement('div');
    card.className = 'video-card';
    
    const thumbnail = document.createElement('div');
    thumbnail.className = 'video-thumbnail';
    
    // Use actual thumbnail if available, otherwise use gradient background
    if (video.thumbnail && video.thumbnail.trim() !== '') {
        thumbnail.style.backgroundImage = `url('${video.thumbnail}')`;
        thumbnail.style.backgroundSize = 'cover';
        thumbnail.style.backgroundPosition = 'center';
        thumbnail.style.backgroundRepeat = 'no-repeat';
    }
    
    // Add trending rank badge
    const rankBadge = document.createElement('div');
    rankBadge.className = 'rank-badge';
    rankBadge.textContent = `#${rank}`;
    thumbnail.appendChild(rankBadge);
    
    const playIcon = document.createElement('div');
    playIcon.className = 'play-icon';
    playIcon.innerHTML = '▶';
    thumbnail.appendChild(playIcon);
    
    const info = document.createElement('div');
    info.className = 'video-info';
    
    const title = document.createElement('h3');
    title.className = 'video-title';
    title.textContent = video.title || 'Untitled Video';
    
    const meta = document.createElement('div');
    meta.className = 'video-meta';
    
    const duration = document.createElement('span');
    duration.className = 'video-duration';
    duration.textContent = video.duration || 'N/A';
    
    const views = document.createElement('span');
    views.className = 'video-views';
    views.textContent = video.views || 'N/A';
    
    const trendingIcon = document.createElement('span');
    trendingIcon.className = 'trending-icon';
    trendingIcon.textContent = '🔥';
    trendingIcon.title = 'Trending';
    trendingIcon.style.fontSize = '14px';
    
    meta.appendChild(trendingIcon);
    meta.appendChild(duration);
    meta.appendChild(views);
    
    info.appendChild(title);
    info.appendChild(meta);
    
    card.appendChild(thumbnail);
    card.appendChild(info);
    
    card.addEventListener('click', () => openModal(video));
    
    return card;
}

// Open Video Modal
function openModal(video) {
    currentVideo = video;
    
    console.log('Opening trending video modal:', video);
    
    if (video.embed_url) {
        modalVideo.innerHTML = `<iframe src="${video.embed_url}" width="100%" height="100%" frameborder="0" allowfullscreen allow="autoplay"></iframe>`;
    } else if (video.video_url) {
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
    modalTitle.textContent = video.title || 'Untitled Video';
    modalDuration.textContent = `⏱️ ${video.duration || 'N/A'}`;
    modalViews.textContent = `👁️ ${video.views || 'No views data'}`;
    
    // Display description with fallback
    let description = video.description || video.title || 'This is a trending video!';
    if (video.tags && video.tags.length > 0) {
        description += `\n\nTags: ${Array.isArray(video.tags) ? video.tags.join(', ') : video.tags}`;
    }
    if (video.source) {
        description += `\n\nSource: ${video.source}`;
    }
    modalDescription.textContent = description;
    
    // Check if already in list
    const myList = JSON.parse(localStorage.getItem('watchLater') || '[]');
    const isInList = myList.some(v => (v.video_url || v.id) === (video.video_url || video.id));
    addToListBtn.textContent = isInList ? '✓ In My List' : '+ Add to My List';
    addToListBtn.disabled = isInList;
    
    videoModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close Modal
function closeModal() {
    videoModal.classList.remove('active');
    modalVideo.innerHTML = '';
    document.body.style.overflow = 'auto';
    currentVideo = null;
}

// Add to My List
function addToMyList() {
    if (!currentVideo) return;
    
    let myList = JSON.parse(localStorage.getItem('watchLater') || '[]');
    
    // Check if already in list
    if (!myList.some(v => (v.video_url || v.id) === (currentVideo.video_url || currentVideo.id))) {
        myList.push(currentVideo);
        localStorage.setItem('watchLater', JSON.stringify(myList));
        addToListBtn.textContent = '✓ In My List';
        addToListBtn.disabled = true;
        
        // Show notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--netflix-red, #e50914);
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
            z-index: 10000;
        `;
        notification.textContent = 'Added to Watch Later!';
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 2000);
    }
}

// Modal Close Events
document.querySelector('.modal-close').addEventListener('click', closeModal);
videoModal.addEventListener('click', (e) => {
    if (e.target === videoModal) closeModal();
});
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && videoModal.classList.contains('active')) {
        closeModal();
    }
});

// Add to List Button
addToListBtn.addEventListener('click', addToMyList);

// Search
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const query = e.target.value.trim();
        if (query) {
            window.location.href = `index.html?search=${encodeURIComponent(query)}`;
        }
    }
});

// Refresh
document.getElementById('refreshBtn').addEventListener('click', () => {
    loadTrendingVideos();
});

// Initialize
loadTrendingVideos();
