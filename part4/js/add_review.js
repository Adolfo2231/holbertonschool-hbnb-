/**
 * Add Review functionality
 */

// API configuration
const API_URL = 'http://127.0.0.1:5000/api/v1';

// Check authentication on page load
const token = window.auth.getCookie('token');
if (!token) {
    window.location.href = 'login.html';
}

// Get place ID from URL parameters
const urlParams = new URLSearchParams(window.location.search);
const placeId = urlParams.get('id');

// Redirect if no place ID is provided
if (!placeId) {
    window.location.href = 'index.html';
}

/**
 * Clear error message display
 */
function clearError() {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = '';
        errorDiv.classList.remove('show-error');
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
 * Display error message to user
 * @param {string} message - Error message to display
 */
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.add('show-error');
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

/**
 * Load place details to show in the form
 */
async function loadPlaceDetails() {
    try {
        // First get the place details
        const placeResponse = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        if (!placeResponse.ok) {
            const data = await placeResponse.json();
            throw new Error(extractErrorMessage(data));
        }

        const place = await placeResponse.json();
        
        // Update page title and place name
        const placeNameElement = document.getElementById('place-name');
        if (placeNameElement) {
            const title = place.title || place.name || 'Unnamed Place';
            placeNameElement.textContent = `Review for ${title}`;
            document.title = `Add Review - ${title}`;
        }

        // Set up back button link
        const backButton = document.getElementById('back-to-place');
        if (backButton) {
            backButton.href = `place.html?id=${placeId}`;
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Error loading place details. Please try again later.');
    }
}

/**
 * Submit review to backend
 * @param {Event} event - Form submission event
 */
async function handleReviewSubmission(event) {
    event.preventDefault();
    clearError();

    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
    }

    try {
        const ratingInput = document.getElementById('rating');
        const textInput = document.getElementById('text');

        if (!ratingInput || !textInput) {
            throw new Error('Form fields not found');
        }

        const rating = parseInt(ratingInput.value);
        const text = textInput.value.trim();

        // Validate rating
        if (!rating || rating < 1 || rating > 5) {
            throw new Error('Please select a valid rating between 1 and 5');
        }

        // Validate text
        if (!text) {
            throw new Error('Please enter your review text');
        }
        if (text.length > 1000) {
            throw new Error('Review text must be 1000 characters or less');
        }

        // Submit the review using the endpoint with JWT authentication
        const response = await fetch(`${API_URL}/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: text,
                rating: rating
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(extractErrorMessage(data));
        }

        // Show success message and redirect
        alert('Review submitted successfully!');
        window.location.href = `place.html?id=${placeId}`;
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred while submitting your review');
    } finally {
        if (submitButton) {
            submitButton.disabled = false;
        }
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    window.auth.checkAuthentication();
    loadPlaceDetails();

    const form = document.getElementById('review-form');
    if (form) {
        form.addEventListener('submit', handleReviewSubmission);
    }
});
  