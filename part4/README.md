# HBnB - Part4 Frontend Implementation

## Overview
This document describes the frontend implementation of the HBnB project (Part4), which includes a modern web interface for property listing, user authentication, and review management.

## Author
Adolfo Rodriguez Castro

## Project Structure
```
part4/
├── css/
│   └── styles.css
├── js/
│   ├── auth.js
│   ├── index.js
│   ├── login.js
│   ├── register.js
│   ├── place.js
│   └── add_review.js
├── img/
├── add_review.html
├── index.html
├── login.html
├── place.html
└── register.html
```

## Features

### 1. Authentication System
- **Login/Register**: Secure user authentication with JWT tokens
- **Session Management**: Persistent user sessions with cookie-based token storage
- **Protected Routes**: Authentication-aware navigation and access control

### 2. Places Management
- **Listing View**: Dynamic grid of available properties
- **Price Filtering**: Interactive price range filtering
- **Detailed View**: Comprehensive property information display
- **Amenities Integration**: Selection and display of property features

### 3. Reviews System
- **Rating Interface**: 5-star rating system
- **Review Submission**: Form for adding property reviews
- **Reviews Display**: Organized display of user reviews
- **User-Specific Management**: Review editing and deletion capabilities

### 4. User Interface
- **Responsive Design**: Mobile-friendly layouts
- **Modern Styling**: Clean and intuitive interface
- **Interactive Elements**: Dynamic content updates
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback for async operations

## Technical Implementation

### HTML Structure
- Semantic HTML5 markup
- Modular component design
- Form validation
- Dynamic content loading

### CSS Implementation
- CSS variables for consistent theming
- Flexbox and Grid layouts
- Responsive design patterns
- Modern UI components
- Cross-page style consistency

### JavaScript Features
- Async/Await for API calls
- Comprehensive error handling
- Form validation
- Dynamic content updates
- Event management
- Token handling

## API Integration
The frontend communicates with the following API endpoints:

| Frontend Action | API Endpoint | Method |
|----------------|--------------|--------|
| User Login | /auth/login | POST |
| User Registration | /users | POST |
| List Places | /places | GET |
| Place Details | /places/{id} | GET |
| Add Review | /places/{id}/reviews | POST |
| List Reviews | /places/{id}/reviews | GET |

## Security Measures
- JWT token storage in secure cookies
- Protected API endpoint access
- Form input validation
- Error message handling
- User input sanitization

## Performance Optimizations
- Image lazy loading
- Efficient DOM updates
- Optimized API calls
- Caching strategies
- Responsive image handling

## Browser Compatibility
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Dependencies
- Font Awesome 5.15.4 (for icons)
- Custom CSS framework
- Vanilla JavaScript

## Getting Started
1. Clone the repository
2. Open `index.html` in a web browser
3. Register a new account or login with existing credentials
4. Start exploring properties and features

## Contributing
Please follow the project's coding standards and submit pull requests for any improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.