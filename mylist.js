// My List Page JavaScript

// DOM Elements
const emptyState = document.getElementById('emptyState');
const myListSection = document.getElementById('myListSection');
const myListVideos = document.getElementById('myListVideos');
const videoCount = document.getElementById('videoCount');
const videoModal = document.getElementById('videoModal');
const modalVideo = document.getElementById('modalVideo');
const modalTitle = document.getElementById('modalTitle');
const modalDuration = document.getElementById('modalDuration');
const modalViews = document.getElementById('modalViews');
const modalDescription = document.getElementById('modalDescription');
const removeFromListBtn = document.getElementById('removeFromListBtn');
const clearListBtn = document.getElementById('clearListBtn');
const sortBtn = document.getElementById('sortBtn');
const confirmModal = document.getElementById('confirmModal');
const confirmClearBtn = document.getElementById('confirmClearBtn');
const cancelClearBtn = document.getElementById('cancelClearBtn');

let currentVideo = null;
let currentSortMode = 'recent'; // recent, title, duration

// Load My List
function loadMyList() {
    const myList = JSON.parse(localStorage.getItem('watchLater') || '[]');
    
    if (myList.length === 0) {
        emptyState.style.display = 'flex';
        myListSection.style.display = 'none';
    } else {
        emptyState.style.display = 'none';
        myListSection.style.display = 'block';
        videoCount.textContent = myList.length;
        displayVideos(myList);
    }
}

// Display Videos
function displayVideos(videos) {
    myListVideos.innerHTML = '';
    
    videos.forEach((video, index) => {
        const videoCard = createVideoCard(video, index);
        myListVideos.appendChild(videoCard);
    });
}

// Create Video Card
function createVideoCard(video, index) {
    const card = document.createElement('div');
    card.className = 'video-card';
    card.dataset.index = index;
    
    const thumbnail = document.createElement('div');
    thumbnail.className = 'video-thumbnail';
    if (video.thumbnail) {
        thumbnail.style.backgroundImage = `url('${video.thumbnail}')`;
    }
    
    // Add remove button
    const removeBtn = document.createElement('button');
    removeBtn.className = 'remove-btn';
    removeBtn.innerHTML = '✕';
    removeBtn.title = 'Remove from list';
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        removeVideo(index);
    });
    thumbnail.appendChild(removeBtn);
    
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
    
    meta.appendChild(duration);
    meta.appendChild(views);
    
    info.appendChild(title);
    info.appendChild(meta);
    
    card.appendChild(thumbnail);
    card.appendChild(info);
    
    card.addEventListener('click', () => openModal(video, index));
    
    return card;
}

// Open Video Modal
function openModal(video, index) {
    currentVideo = { video, index };
    
    if (video.embed_url) {
        modalVideo.innerHTML = `<iframe src="${video.embed_url}" width="100%" height="100%" frameborder="0" allowfullscreen allow="autoplay"></iframe>`;
    } else {
        modalVideo.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#999;">Video not available</div>';
    }
    
    modalTitle.textContent = video.title || 'Untitled Video';
    modalDuration.textContent = video.duration || 'N/A';
    modalViews.textContent = video.views || 'No views data';
    modalDescription.textContent = video.description || 'No description available.';
    
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

// Remove Video from List
function removeVideo(index) {
    let myList = JSON.parse(localStorage.getItem('watchLater') || '[]');
    myList.splice(index, 1);
    localStorage.setItem('watchLater', JSON.stringify(myList));
    loadMyList();
}

// Remove Current Video from Modal
function removeCurrentVideo() {
    if (!currentVideo) return;
    removeVideo(currentVideo.index);
    closeModal();
}

// Clear All Videos
function clearAllVideos() {
    localStorage.setItem('watchLater', JSON.stringify([]));
    loadMyList();
    confirmModal.classList.remove('active');
}

// Show Confirmation Modal
function showConfirmModal() {
    confirmModal.classList.add('active');
}

// Hide Confirmation Modal
function hideConfirmModal() {
    confirmModal.classList.remove('active');
}

// Sort Videos
function sortVideos() {
    let myList = JSON.parse(localStorage.getItem('watchLater') || '[]');
    
    if (currentSortMode === 'recent') {
        // Sort by title
        myList.sort((a, b) => a.title.localeCompare(b.title));
        currentSortMode = 'title';
        sortBtn.textContent = 'Sort: Title (A-Z) ▼';
    } else if (currentSortMode === 'title') {
        // Sort by title reverse
        myList.sort((a, b) => b.title.localeCompare(a.title));
        currentSortMode = 'title-reverse';
        sortBtn.textContent = 'Sort: Title (Z-A) ▼';
    } else {
        // Back to recent (reverse array to show newest first)
        myList.reverse();
        currentSortMode = 'recent';
        sortBtn.textContent = 'Sort: Recently Added ▼';
    }
    
    displayVideos(myList);
}

// Modal Close Events
document.querySelector('.modal-close').addEventListener('click', closeModal);
videoModal.addEventListener('click', (e) => {
    if (e.target === videoModal) closeModal();
});
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (videoModal.classList.contains('active')) {
            closeModal();
        }
        if (confirmModal.classList.contains('active')) {
            hideConfirmModal();
        }
    }
});

// Button Events
removeFromListBtn.addEventListener('click', removeCurrentVideo);
clearListBtn.addEventListener('click', showConfirmModal);
confirmClearBtn.addEventListener('click', clearAllVideos);
cancelClearBtn.addEventListener('click', hideConfirmModal);
sortBtn.addEventListener('click', sortVideos);

// Search
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const query = e.target.value.trim();
        if (query) {
            window.location.href = `index.html?search=${encodeURIComponent(query)}`;
        }
    }
});

// Initialize
loadMyList();
