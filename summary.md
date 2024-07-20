# DealerSync Application Structure

## Frontend (React)

### `/dealer_sync_frontend`
Main frontend directory

#### `/src`
Source code for the React application

- `App.js`: Main component, sets up routing and authentication
- `index.js`: Entry point of the React application
- `index.css`: Global styles

##### `/components`
Reusable React components

- `Card.js`: Card component for consistent styling
- `CardContent.js`: Content area for Card component
- `CardHeader.js`: Header area for Card component
- `CardTitle.js`: Title component for Card headers
- `Layout.js`: Main layout component with navigation
- `ProtectedRoute.js`: Route wrapper for authentication

##### `/views`
Main page components

- `Auth.js`: Authentication page (login/register)
- `Dashboard.js`: Main dashboard view
- `Listings.js`: Vehicle listings page
- `Sync.js`: Synchronization control and status page

##### `/store`
Redux store setup

- `store.js`: Redux store configuration
- `syncSlice.js`: Redux slice for sync-related state

##### `/tests`
Frontend test files

- `Auth.test.js`: Tests for Auth component
- `Dashboard.test.js`: Tests for Dashboard component
- `Sync.test.js`: Tests for Sync component

#### `/public`
Public assets and HTML template

#### `/mocks`
Mock files for testing

## Backend (Django)

### `/dealer_sync_backend`
Main backend directory

#### `/dealer_sync_backend`
Django project configuration

- `settings.py`: Django settings file
- `urls.py`: Main URL configuration
- `celery.py`: Celery configuration for background tasks

#### `/authentication`
Authentication app

- `views.py`: Authentication-related views
- `urls.py`: URL patterns for authentication
- `serializers.py`: Serializers for user data

#### `/dashboard`
Dashboard app

- `views.py`: Views for dashboard data
- `urls.py`: URL patterns for dashboard
- `serializers.py`: Serializers for dashboard data

#### `/scraper`
Web scraping app

- `views.py`: Views for scraper control and data
- `urls.py`: URL patterns for scraper
- `models.py`: Database models for vehicle listings and sync attempts
- `scraper.py`: Web scraping logic
- `tasks.py`: Celery tasks for background scraping

##### `/management/commands`
Custom Django management commands

- `check_database.py`: Command to check database content

### Root Files

- `manage.py`: Django management script
- `requirements.txt`: Python package dependencies

## Summary

DealerSync is a web application for managing vehicle listings. It consists of a React frontend and a Django backend. The frontend includes components for authentication, dashboard, listings, and synchronization control. The backend is divided into apps for authentication, dashboard data, and web scraping. It uses Celery for background tasks and includes custom management commands for database operations.

Key features:
- User authentication
- Vehicle listing management
- Web scraping for vehicle data
- Dashboard with statistics and charts
- Synchronization control and monitoring

The application uses modern web technologies and follows a modular structure for both frontend and backend, allowing for easy maintenance and scalability.
