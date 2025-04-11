/**
 * Login page functionality
 */

// API configuration
const API_URL = 'http://127.0.0.1:5000/api/v1';

/**
 * Show error message to user
 * @param {string} message - Error message to display
 */
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

/**
 * Clear error message
 */
function clearError() {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = '';
    errorDiv.style.display = 'none';
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
 * Handle login form submission
 * @param {Event} event - Form submission event
 */
async function handleLogin(event) {
    event.preventDefault();
    clearError();

    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
    }

    try {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(extractErrorMessage(data));
        }

        // Guardar el token en la cookie si el login fue exitoso
        if (data.access_token) {
            window.auth.setCookie('token', data.access_token);
            window.location.href = 'index.html';
        } else {
            throw new Error('No token received from server');
        }

    } catch (error) {
        console.error('Login error:', error);
        showError(error.message || 'Login failed. Please try again.');
    } finally {
        if (submitButton) {
            submitButton.disabled = false;
        }
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    if (form) {
        form.addEventListener('submit', handleLogin);
    }

    // Si ya hay un token válido, redirigir a index
    const token = window.auth.getCookie('token');
    if (token) {
        window.location.href = 'index.html';
    }
}); 