/**
 * @file index.js
 * @description Main JavaScript file for handling places listing and filtering functionality
 */

// API configuration
const API_URL = 'http://127.0.0.1:5000/api/v1';

// Verificar si el usuario es administrador
function checkAdminAccess() {
    const token = window.auth.getCookie('token');
    if (!token) return false;

    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        const tokenPayload = JSON.parse(jsonPayload);
        return tokenPayload.role === 'admin';
    } catch (error) {
        console.error('Error checking admin role:', error);
        return false;
    }
}

/**
 * Format price with currency symbol
 * @param {number} price - Price to format
 * @returns {string} Formatted price
 */
function formatPrice(price) {
    return `$${price.toFixed(2)}`;
}

/**
 * Create HTML for amenities list
 * @param {Array} amenities - List of amenities
 * @returns {string} HTML string for amenities
 */
function createAmenitiesHtml(amenities) {
    if (!amenities || amenities.length === 0) return '';
    
    return `
        <div class="amenities-list">
            ${amenities.map(amenity => `
                <span class="amenity-pill">${amenity.name}</span>
            `).join('')}
        </div>
    `;
}

/**
 * Create HTML for a place card
 * @param {Object} place - Place data
 * @returns {string} HTML string for place card
 */
function createPlaceCard(place) {
    const title = place.title || place.name || "Unnamed Place";
    const imageName = `${title.replace(/\s+/g, '_')}.png`;
    const description = place.description || "No description available";
    const price = place.price || place.price_by_night || 0;
    const amenitiesHtml = createAmenitiesHtml(place.amenities);
    
    return `
        <div class="place-card" data-price="${price}">
            <img src="img/${imageName}" 
                alt="${title}" 
                style="width: 100%; height: 200px; object-fit: cover;"
                onerror="this.onerror=null; this.src='img/default.png'">
            <div class="place-info">
                <h2>${title}</h2>
                <p class="price"><strong>Price per night:</strong> ${formatPrice(price)}</p>
                <p class="description">${description.length > 100 ? description.substring(0, 97) + '...' : description}</p>
                ${amenitiesHtml}
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        </div>
    `;
}

/**
 * Display places in the container
 * @param {Array} places - List of places to display
 */
function displayPlaces(places) {
    const container = document.querySelector('.places-container');
    if (!container) return;
    
    if (!places || places.length === 0) {
        container.innerHTML = '<p class="text-center">No places found</p>';
        return;
    }

    container.innerHTML = places.map(place => createPlaceCard(place)).join('');
    applyPriceFilter();
}

/**
 * Filter places by maximum price
 */
function applyPriceFilter() {
    const maxPrice = document.getElementById('max-price');
    if (!maxPrice) return;

    const value = maxPrice.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));
        if (value === 'all' || price <= parseFloat(value)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
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
 * Load and display places from the backend
 */
async function fetchPlaces() {
    try {
        const token = window.auth.getCookie('token');
        const response = await fetch(`${API_URL}/places/`, {
            headers: {
                'Authorization': token ? `Bearer ${token}` : ''
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(extractErrorMessage(data));
        }

        const result = await response.json();
        
        // Store places in global variable for filtering
        window.places = result.data;
        
        // Display places
        displayPlaces(result.data);
        
        // Show admin actions if user is admin
        const isAdmin = checkAdminAccess();
        const adminActions = document.getElementById('admin-actions');
        if (adminActions) {
            adminActions.style.display = isAdmin ? 'block' : 'none';
        }
    } catch (error) {
        console.error('Error:', error);
        const container = document.querySelector('.places-container');
        if (container) {
            container.innerHTML = '<p class="error-message">Error loading places. Please try again later.</p>';
        }
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is authenticated
    const token = window.auth.getCookie('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    window.auth.checkAuthentication();
    fetchPlaces();
    
    const maxPrice = document.getElementById('max-price');
    if (maxPrice) {
        maxPrice.addEventListener('change', applyPriceFilter);
    }
});
