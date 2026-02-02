// Categories Page JavaScript
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const categoriesGrid = document.getElementById('categoriesGrid');
const categoryVideosSection = document.getElementById('categoryVideosSection');
const categoryVideos = document.getElementById('categoryVideos');
const categoryTitle = document.getElementById('categoryTitle');
const backToCategories = document.getElementById('backToCategories');
const loadingState = document.getElementById('loadingState');
const noVideosMessage = document.getElementById('noVideosMessage');
const videoModal = document.getElementById('videoModal');
const modalVideo = document.getElementById('modalVideo');
const modalTitle = document.getElementById('modalTitle');
const modalDuration = document.getElementById('modalDuration');
const modalViews = document.getElementById('modalViews');
const modalDescription = document.getElementById('modalDescription');
const addToListBtn = document.getElementById('addToListBtn');

let currentVideo = null;

// Load Categories
async function loadCategories() {
    try {
        loadingState.style.display = 'flex';
        categoriesGrid.style.display = 'none';

        const response = await fetch(`${API_BASE_URL}/categories`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();

        if (data.success && data.categories) {
            displayCategories(data.categories);
        } else {
            throw new Error('No categories data received');
        }
    } catch (error) {
        console.error('Error loading categories:', error);
        loadingState.innerHTML = `<div class="error-message"><h3>Oops!</h3><p>Failed to load categories. Please check your connection and try again.</p><button onclick="location.reload()">Retry</button></div>`;
    }
}

// Display Categories
function displayCategories(categories) {
    categoriesGrid.innerHTML = '';
    
    if (!categories || categories.length === 0) {
        loadingState.innerHTML = '<p style="color: #e50914;">No categories available</p>';
        return;
    }
    
    categories.forEach((category, index) => {
        const categoryCard = document.createElement('div');
        categoryCard.className = 'category-card';
        categoryCard.style.animationDelay = `${index * 0.05}s`;
        categoryCard.innerHTML = `
            <div class="category-icon">${category.icon}</div>
            <div class="category-name">${category.name}</div>
        `;
        categoryCard.addEventListener('click', () => loadCategoryVideos(category));
        categoriesGrid.appendChild(categoryCard);
    });

    loadingState.style.display = 'none';
    categoriesGrid.style.display = 'grid';
}

// Load Videos by Category
async function loadCategoryVideos(category) {
    try {
        // Hide categories, show loading
        categoriesGrid.style.display = 'none';
        categoryVideosSection.style.display = 'block';
        categoryTitle.textContent = `${category.icon} ${category.name}`;
        categoryVideos.innerHTML = '<div class="loading-container"><div class="loading-spinner"></div><p>Loading videos...</p></div>';
        noVideosMessage.style.display = 'none';

        const response = await fetch(`${API_BASE_URL}/categories/${category.id}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();

        if (data.success && data.videos && data.videos.length > 0) {
            displayCategoryVideos(data.videos);
        } else {
            categoryVideos.innerHTML = '';
            noVideosMessage.style.display = 'block';
            noVideosMessage.innerHTML = '<p>No videos found in this category. Try another one!</p>';
        }
    } catch (error) {
        console.error('Error loading category videos:', error);
        categoryVideos.innerHTML = `<div class="error-message"><h3>Oops!</h3><p>Failed to load videos for this category. Please try again later.</p></div>`;
    }
}

// Display Category Videos
function displayCategoryVideos(videos) {
    categoryVideos.innerHTML = '';
    
    videos.forEach(video => {
        const videoCard = createVideoCard(video);
        categoryVideos.appendChild(videoCard);
    });
}

// Create Video Card
function createVideoCard(video) {
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
    
    const playIcon = document.createElement('div');
    playIcon.className = 'play-icon';
    playIcon.innerHTML = '▶';
    thumbnail.appendChild(playIcon);
    
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
    views.textContent = video.views || 'N/A';
    
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
    
    console.log('Opening category video modal:', video);
    
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
    let description = video.description || video.title || 'No description available.';
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

// Back to Categories
backToCategories.addEventListener('click', () => {
    categoryVideosSection.style.display = 'none';
    categoriesGrid.style.display = 'grid';
});

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
    location.reload();
});

// Initialize
loadCategories();
