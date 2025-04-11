/**
 * Place details and reviews functionality
 */

// API configuration
const API_URL = 'http://127.0.0.1:5000/api/v1';

// Get place ID from URL parameters
const urlParams = new URLSearchParams(window.location.search);
const placeId = urlParams.get('id');

// Redirect if no place ID is provided
if (!placeId) {
    window.location.href = 'index.html';
}

/**
 * Format price with currency symbol
 * @param {number} price - Price to format
 * @returns {string} Formatted price
 */
function formatPrice(price) {
    return `$${Number(price).toFixed(2)}`;
}

/**
 * Create HTML for amenities list
 * @param {Array} amenities - List of amenities
 * @returns {string} HTML string for amenities
 */
function createAmenitiesHtml(amenities) {
    if (!amenities || amenities.length === 0) {
        return '<p class="no-amenities">No amenities listed</p>';
    }
    
    return `
        <div class="amenities-list">
            ${amenities.map(amenity => `
                <span class="amenity-pill">${amenity.name}</span>
            `).join('')}
        </div>
    `;
}

/**
 * Create star rating HTML
 * @param {number} rating - Rating value (1-5)
 * @returns {string} HTML string for star rating
 */
function createStarRating(rating) {
    const fullStar = '★';
    const emptyStar = '☆';
    const ratingValue = Math.min(Math.max(parseInt(rating) || 0, 0), 5);
    const stars = fullStar.repeat(ratingValue) + emptyStar.repeat(5 - ratingValue);
    return `<div class="rating" title="${ratingValue} out of 5 stars">${stars}</div>`;
}

/**
 * Format date to locale string
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    try {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    } catch (error) {
        console.error('Error formatting date:', error);
        return 'Invalid date';
    }
}

/**
 * Create HTML for a review
 * @param {Object} review - Review data
 * @returns {string} HTML string for review
 */
function createReviewHtml(review) {
    const date = formatDate(review.created_at);
    const rating = parseInt(review.rating) || 0;
    const text = review.text || 'No comment provided';

    return `
        <div class="review-card">
            <div class="review-header">
                <div class="review-user-info">
                    ${review.user?.name ? `<p class="user-name">${review.user.name}</p>` : ''}
                    <span class="review-date">${date}</span>
                </div>
                ${createStarRating(rating)}
            </div>
            <p class="review-text">${text}</p>
        </div>
    `;
}

/**
 * Display place details in the container
 * @param {Object} place - Place data
 */
function displayPlaceDetails(place) {
    const detailsContainer = document.getElementById('place-details');
    if (!detailsContainer) {
        console.error('Place details container not found');
        return;
    }

    const title = place.title || place.name || "Unnamed Place";
    const imageName = `${title.replace(/\s+/g, '_')}.png`;
    const description = place.description || "No description available";
    const price = place.price || place.price_by_night || 0;
    
    detailsContainer.innerHTML = `
        <div class="place-header">
            <div class="place-image-container">
                <img src="img/${imageName}" 
                    alt="${title}" 
                    class="place-image"
                    onerror="this.onerror=null; this.src='img/default.png'">
            </div>
            <div class="place-info">
                <h1>${title}</h1>
                <p class="price">Price per night: ${formatPrice(price)}</p>
                <p class="description">${description}</p>
                
                <h2>Amenities</h2>
                ${createAmenitiesHtml(place.amenities)}
                
                ${window.auth.getCookie('token') ? 
                    `<a href="add_review.html?id=${place.id}" class="details-button mt-3">Add Review</a>` : 
                    `<a href="login.html" class="details-button mt-3">Login to Add Review</a>`}
            </div>
        </div>
    `;

    // Update page title
    document.title = `${title} - HBNB`;
}

/**
 * Display reviews in the container
 * @param {Array} reviews - List of reviews
 */
function displayReviews(reviews) {
    const container = document.getElementById('reviews-container');
    if (!container) {
        console.error('Reviews container not found');
        return;
    }
    
    if (!reviews || !Array.isArray(reviews) || reviews.length === 0) {
        container.innerHTML = '<p class="no-reviews">No reviews yet. Be the first to review!</p>';
        return;
    }
    
    container.innerHTML = `
        <div class="reviews-list">
            ${reviews.map(review => createReviewHtml(review)).join('')}
        </div>
    `;
}

/**
 * Show error message
 * @param {string} message - Error message to display
 * @param {string} containerId - ID of container to show error in
 */
function showError(message, containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="error-message">${message}</div>`;
    }
}

/**
 * Extract error message from response data
 * @param {Object} data - Response data
 * @returns {string} Error message
 */
function extractErrorMessage(data) {
    if (data.message?.message?.status === "error") {
        return data.message.message.details || data.message.message.message;
    }
    if (typeof data.message === 'string') {
        return data.message;
    }
    if (typeof data.message === 'object') {
        return data.message.message || data.message.error || JSON.stringify(data.message);
    }
    return 'An unexpected error occurred';
}

/**
 * Load place details from the backend
 */
async function loadPlaceDetails() {
    const token = window.auth.getCookie('token');
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(extractErrorMessage(data));
        }

        displayPlaceDetails(data);
        
        // Load reviews after place details are loaded
        loadReviews();
    } catch (error) {
        console.error('Error loading place details:', error);
        showError('Error loading place details. Please try again later.', 'place-details');
    }
}

/**
 * Load reviews from the backend
 */
async function loadReviews() {
    const token = window.auth.getCookie('token');
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_URL}/places/${placeId}/reviews`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(extractErrorMessage(data));
        }

        // Acceder correctamente a las reviews en la estructura de datos
        const reviews = data.data?.reviews || [];
        
        displayReviews(reviews);
    } catch (error) {
        console.error('Error loading reviews:', error);
        showError('Error loading reviews.', 'reviews-container');
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication
    window.auth.checkAuthentication();

    // Load data
    loadPlaceDetails();
});
  