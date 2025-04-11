/**
 * User Registration functionality
 */

// API configuration
const API_URL = 'http://127.0.0.1:5000/api/v1';

/**
 * Display error message to user
 * @param {string} message - Error message to display
 */
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.classList.add('show-error');
    
    // Scroll to error message
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Display success message to user
 * @param {string} message - Success message to display
 */
function showSuccess(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.backgroundColor = '#d4edda';
    errorDiv.style.color = '#155724';
    errorDiv.classList.add('show-error');
    
    // Scroll to message
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Clear error message display
 */
function clearError() {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = '';
    errorDiv.classList.remove('show-error');
}

/**
 * Handle registration form submission
 * @param {Event} event - Form submission event
 */
async function handleRegistration(event) {
    event.preventDefault();
    clearError();

    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    try {
        const formData = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            first_name: document.getElementById('first_name').value,
            last_name: document.getElementById('last_name').value
        };

        const response = await fetch(`${API_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            let errorMessage;
            
            if (data.message?.message?.status === "error") {
                errorMessage = data.message.message.details || data.message.message.message;
            }
            else if (typeof data.message === 'string') {
                errorMessage = data.message;
            }
            else if (typeof data.message === 'object') {
                errorMessage = data.message.message || data.message.error || JSON.stringify(data.message);
            }
            else {
                errorMessage = 'Registration failed';
            }
            
            throw new Error(errorMessage);
        }

        // Show success message and redirect after delay
        showSuccess('¡Usuario creado exitosamente! Redirigiendo al login...');
        setTimeout(() => {
            window.location.replace('login.html');
        }, 2000);
    } catch (error) {
        showError(error.message || 'Registration failed. Please try again.');
        submitButton.disabled = false;
    }
}

// Initialize registration form
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegistration);
    }
}); 