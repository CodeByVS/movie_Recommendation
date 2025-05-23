// Enhanced search functionality with smooth transition
document.querySelector('.search-button').addEventListener('click', function() {
    const query = document.querySelector('.search-input').value.trim().toLowerCase();
    if (query) {
        localStorage.setItem('movieSearchQuery', query);
        window.location.href = '/search?query=' + encodeURIComponent(query);
    } else {
        // Show a subtle animation for empty search
        const searchInput = document.querySelector('.search-input');
        searchInput.classList.add('shake');
        setTimeout(() => searchInput.classList.remove('shake'), 500);
        searchInput.placeholder = 'Please enter a search term...';
        searchInput.focus();
    }
});

document.querySelector('.search-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        const query = this.value.trim().toLowerCase();
        if (query) {
            localStorage.setItem('movieSearchQuery', query);
            window.location.href = '/search?query=' + encodeURIComponent(query);
        } else {
            // Show a subtle animation for empty search
            this.classList.add('shake');
            setTimeout(() => this.classList.remove('shake'), 500);
            this.placeholder = 'Please enter a search term...';
        }
    }
});

// Smooth scrolling for menu items
document.querySelectorAll('.menu-list-item').forEach(item => {
    item.addEventListener('click', function(e) {
        // Remove 'active' class from all items
        document.querySelectorAll('.menu-list-item').forEach(i => i.classList.remove('active'));
        
        // Add 'active' class to clicked item
        this.classList.add('active');
        
        if (this.textContent !== 'Home') {
            // Only scroll for non-home items on the same page
            e.preventDefault();
            
            // Get the corresponding section to scroll to
            const section = document.querySelector(`#${this.textContent.toLowerCase()}`);
            if (section) {
                window.scrollTo({
                    top: section.offsetTop - 80,  // Offset for navbar
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Remove slider functionality and display all movies in a grid
document.addEventListener('DOMContentLoaded', () => {
    // Convert movie lists to grid layout
    document.querySelectorAll('.movie-list').forEach(list => {
        list.style.display = 'grid';
        list.style.gridTemplateColumns = 'repeat(auto-fill, minmax(280px, 1fr))';
        list.style.gap = '25px';
        list.style.transform = 'none';
        list.style.height = 'auto';
    });
    
    // Remove arrows
    document.querySelectorAll('.arrow, .cool-arrow').forEach(arrow => {
        arrow.style.display = 'none';
    });
    
    // Adjust movie list wrapper
    document.querySelectorAll('.movie-list-wrapper').forEach(wrapper => {
        wrapper.style.overflow = 'visible';
        wrapper.style.marginRight = '0';
    });
    
    // Enhanced slider functionality for movie lists
    const arrows = document.querySelectorAll(".arrow");
    const movieLists = document.querySelectorAll(".movie-list");
    
    arrows.forEach((arrow, i) => {
        const itemNumber = movieLists[i].querySelectorAll(".movie-list-item").length;
        let clickCounter = 0;
        
        // Update arrow to use cool styling
        arrow.innerHTML = '<i class="fas fa-chevron-right"></i>';
        arrow.classList.add('cool-arrow');
        
        arrow.addEventListener("click", () => {
            const ratio = Math.floor(window.innerWidth / 280);
            const visibleItems = Math.min(ratio, 5); // Limit to 5 visible items max
            clickCounter++;
            
            if (itemNumber - (visibleItems + clickCounter) + (visibleItems - ratio) >= 0) {
                // Smooth sliding animation
                movieLists[i].style.transform = `translateX(${
                    movieLists[i].computedStyleMap().get("transform")[0].x.value - 300
                }px)`;
            } else {
                // Reset to beginning with smooth animation
                movieLists[i].style.transform = "translateX(0)";
                clickCounter = 0;
            }
            
            // Add a subtle animation to the arrow
            arrow.classList.add('arrow-clicked');
            setTimeout(() => {
                arrow.classList.remove('arrow-clicked');
            }, 300);
        });
    });
    
    // If no preference is set, default to dark mode
    if (localStorage.getItem('darkMode') === null) {
        setThemePreference(true);
    }
    
    applyTheme();
    
    // Add animation to featured content
    const featuredContent = document.querySelector('.featured-content');
    if (featuredContent) {
        setTimeout(() => {
            featuredContent.classList.add('fade-in');
        }, 300);
    }
    
    // Staggered animation for movie cards
    const movieItems = document.querySelectorAll('.movie-list-item');
    movieItems.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('fade-in');
        }, 150 * (index % 7)); // Stagger based on position in row
    });
});

// Theme is permanently set to dark mode
const body = document.body;

// Ensure dark mode is always enabled
function setDarkMode() {
    localStorage.setItem('darkMode', 'enabled');
    body.classList.add("dark-mode");
}

// Apply theme on page load
document.addEventListener('DOMContentLoaded', () => {
    // Remove the grid layout code and restore slider functionality
    document.querySelectorAll('.movie-list').forEach(list => {
        list.style.display = 'flex';
        list.style.gridTemplateColumns = '';
        list.style.gap = '';
        list.style.transform = 'translateX(0)';
        list.style.height = '330px';
    });
    
    // Hide all arrows permanently
    document.querySelectorAll('.arrow, .cool-arrow').forEach(arrow => {
        arrow.style.display = 'none';
        arrow.remove(); // Completely remove the arrows from DOM
    });
    
    // Reset movie list wrapper but without margin for arrows
    document.querySelectorAll('.movie-list-wrapper').forEach(wrapper => {
        wrapper.style.overflow = 'hidden';
        wrapper.style.marginRight = '0'; // No margin needed for arrows
    });
    
    // Always set to dark mode
    setDarkMode();
    
    // Add animation to featured content
    const featuredContent = document.querySelector('.featured-content');
    if (featuredContent) {
        setTimeout(() => {
            featuredContent.classList.add('fade-in');
        }, 300);
    }
    
    // Staggered animation for movie cards
    const movieItems = document.querySelectorAll('.movie-list-item');
    movieItems.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('fade-in');
        }, 150 * (index % 7)); // Stagger based on position in row
    });
});

// No toggle functionality - site is always in dark mode

// Add hover effects for movie items - restored to original behavior
document.querySelectorAll('.movie-list-item').forEach(item => {
    // Remove the custom hover event listeners
    item.removeEventListener('mouseenter', function() {});
    item.removeEventListener('mouseleave', function() {});
    
    // Clear any inline styles that might have been applied
    item.style.transform = '';
});

// Add recommendation button functionality
document.addEventListener('DOMContentLoaded', () => {
    // Add click event listeners to all recommendation buttons
    document.querySelectorAll('.recommend-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent bubbling to parent
            const movieTitle = this.dataset.title;
            getRecommendations(movieTitle);
        });
    });
});

// Function to get movie recommendations
function getRecommendations(movieTitle) {
    console.log('Getting recommendations for:', movieTitle);
    
    // Store the movie title in localStorage for the search page
    localStorage.setItem('recommendMovie', movieTitle);
    
    // Redirect to the search page with a special parameter
    window.location.href = '/search?recommend=' + encodeURIComponent(movieTitle);
}

// Add this to your DOMContentLoaded event to ensure it applies on page load
document.addEventListener('DOMContentLoaded', () => {
    // Rest of your existing DOMContentLoaded code...
    
    // Reset any custom styling on movie items
    document.querySelectorAll('.movie-list-item').forEach(item => {
        item.style = '';
        
        const elements = item.querySelectorAll('*');
        elements.forEach(el => {
            el.style = '';
        });
    });
});

// Add click effect for buttons
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', function(e) {
        // Create ripple effect
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        this.appendChild(ripple);
        
        // Position the ripple
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        
        // Remove ripple after animation
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Improve accessibility
document.addEventListener('DOMContentLoaded', () => {
    
    // Add lazy loading to images for better performance
    document.querySelectorAll('.movie-list-item-img').forEach(img => {
        img.setAttribute('loading', 'lazy');
    });
});
