/**
 * Epic Theme Switcher
 * Dark Mode (Red & Black) and Light Mode with smooth transitions
 */

// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = this.getSavedTheme() || 'dark-mode';
        this.themeToggle = document.getElementById('themeToggle');
        this.init();
    }

    init() {
        // Apply saved theme on load
        this.applyTheme(this.currentTheme, false);
        
        // Setup event listener
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Add epic entrance animation
        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 100);
    }

    getSavedTheme() {
        return localStorage.getItem('blueTubeTheme');
    }

    saveTheme(theme) {
        localStorage.setItem('blueTubeTheme', theme);
    }

    applyTheme(theme, animate = true) {
        const body = document.body;
        
        // Remove all theme classes
        body.classList.remove('dark-mode', 'light-mode');
        
        // Add new theme
        body.classList.add(theme);
        
        // Add animation class if needed
        if (animate) {
            body.classList.add('theme-transitioning');
            
            // Create epic transition effect
            this.createTransitionEffect();
            
            setTimeout(() => {
                body.classList.remove('theme-transitioning');
            }, 800);
        }
        
        this.currentTheme = theme;
        this.saveTheme(theme);
        
        // Update toggle button state
        this.updateToggleButton();
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark-mode' ? 'light-mode' : 'dark-mode';
        this.applyTheme(newTheme, true);
        
        // Add rotation animation to button
        if (this.themeToggle) {
            this.themeToggle.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.themeToggle.style.transform = '';
            }, 600);
        }
    }

    updateToggleButton() {
        if (!this.themeToggle) return;
        
        const sunIcon = this.themeToggle.querySelector('.sun-icon');
        const moonIcon = this.themeToggle.querySelector('.moon-icon');
        
        if (this.currentTheme === 'light-mode') {
            if (sunIcon) sunIcon.style.display = 'block';
            if (moonIcon) moonIcon.style.display = 'none';
        } else {
            if (sunIcon) sunIcon.style.display = 'none';
            if (moonIcon) moonIcon.style.display = 'block';
        }
    }

    createTransitionEffect() {
        // Create epic ripple effect
        const ripple = document.createElement('div');
        ripple.className = 'theme-ripple';
        ripple.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: ${this.currentTheme === 'light-mode' ? 
                'radial-gradient(circle, rgba(229,9,20,0.3) 0%, rgba(255,255,255,0.1) 100%)' : 
                'radial-gradient(circle, rgba(0,0,0,0.8) 0%, rgba(229,9,20,0.2) 100%)'};
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 9999;
            animation: rippleExpand 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        `;
        
        document.body.appendChild(ripple);
        
        // Remove ripple after animation
        setTimeout(() => {
            ripple.remove();
        }, 800);
    }
}

// Add ripple animation to stylesheet dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes rippleExpand {
        0% {
            width: 0;
            height: 0;
            opacity: 1;
        }
        100% {
            width: 200vw;
            height: 200vw;
            opacity: 0;
        }
    }
    
    body {
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .theme-transitioning {
        overflow: hidden;
    }
`;
document.head.appendChild(style);

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.themeManager = new ThemeManager();
    });
} else {
    window.themeManager = new ThemeManager();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
