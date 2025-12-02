# User Management Flask Application

## Overview
A Flask web application for managing users with advanced features including search, edit, sorting, validation, and AJAX-based data refresh.

## Features Implemented

### 1. **Search Functionality**
- Search users by name in real-time
- AJAX-based search without page reload
- Case-insensitive search matching

### 2. **Edit/Update Form**
- Modal form to edit existing user details
- Modify email, name, and other user information
- AJAX form submission for seamless updates

### 3. **User Sorting**
- Sort users by name (A-Z, Z-A)
- Sort users by email (A-Z, Z-A)
- Dynamic sorting with AJAX refresh

### 4. **Form Validation**
- Email format validation
- Prevent duplicate email addresses
- Required field validation
- Server-side and client-side validation

### 5. **AJAX Data Refresh**
- Dynamic table updates without page reload
- Asynchronous add/edit/delete operations
- Real-time user list refresh

## Project Structure

```
user-management-app/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── database.db (SQLite)
```

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Access at `http://localhost:5000`

## Dependencies
- Flask
- Flask-SQLAlchemy
- SQLAlchemy

## API Endpoints

- `GET /` - Main page
- `GET /api/users` - Get all users (JSON)
- `POST /api/users` - Create new user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user
- `GET /api/search?query=<name>` - Search users

## Database Schema

### Users Table
- `id` - Primary Key (Integer)
- `name` - User Name (String)
- `email` - User Email (String, Unique)
- `created_at` - Creation Timestamp

## Implementation Notes

All features use AJAX for seamless user experience without page reloads. The application includes both client-side and server-side validation to ensure data integrity.
