/**
 * Authentication utility functions for managing user sessions and cookies
 */

/**
 * Get a cookie value by name
 * @param {string} name - The name of the cookie to retrieve
 * @returns {string|null} The cookie value if found, null otherwise
 */
const getCookie = (name) => {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.split('=').map(c => c.trim());
        if (cookieName === name) {
            return decodeURIComponent(cookieValue);
        }
    }
    return null;
};

/**
 * Set a cookie with the specified name and value
 * @param {string} name - The name of the cookie to set
 * @param {string} value - The value to store in the cookie
 * @param {number} days - Number of days until the cookie expires
 */
const setCookie = (name, value, days = 7) => {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
};

/**
 * Handle user logout
 * Clears authentication token and redirects to login page
 */
const logout = async () => {
    try {
        const token = getCookie('token');
        if (token) {
            await fetch('http://127.0.0.1:5000/api/v1/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
        }
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = 'login.html';
    }
};

/**
 * Check if user is authenticated and update UI accordingly
 * @returns {boolean} True if user is authenticated, false otherwise
 */
const checkAuthentication = () => {
    const token = getCookie('token');
    const authBtn = document.querySelector('.login-button');
    
    if (token) {
        if (authBtn) {
            authBtn.textContent = 'Logout';
            authBtn.href = '#';
            authBtn.onclick = logout;
        }
        return true;
    } else {
        if (authBtn) {
            authBtn.textContent = 'Login';
            authBtn.href = 'login.html';
            authBtn.onclick = null;
        }
        return false;
    }
};

// Export authentication utilities
window.auth = {
    getCookie,
    setCookie,
    logout,
    checkAuthentication,

    /**
     * Get current user information from the server
     * @returns {Promise<Object>} User information
     */
    async getCurrentUser() {
        const token = this.getCookie('token');
        if (!token) return null;

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/protected', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to get user information');
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error getting user information:', error);
            return null;
        }
    },

    /**
     * Get user ID from server or token
     * @returns {Promise<string|null>} User ID
     */
    async getUserId() {
        try {
            const userInfo = await this.getCurrentUser();
            if (userInfo && userInfo.message) {
                // Extraer el ID del mensaje que viene en formato:
                // ["Hello, user:", "Name: ...", "ID: ..."]
                const idMessage = userInfo.message.find(msg => msg.startsWith('ID:'));
                if (idMessage) {
                    return idMessage.split('ID:')[1].trim();
                }
            }
            return null;
        } catch (error) {
            console.error('Error getting user ID:', error);
            return null;
        }
    }
};

// Add logout functionality to logout buttons
document.addEventListener('DOMContentLoaded', () => {
    const logoutButtons = document.querySelectorAll('a[href="#"][class="login-button"]');
    logoutButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            window.auth.logout();
        });
    });
});