# README.md - Fintech Platform

## Overview
This is a fullstack web application for a fintech platform that offers trading signals, bots, and educational resources. The platform includes a modern frontend built with Vue.js and a robust backend powered by Django.

## Features
- User authentication and authorization
- Product marketplace for signals, bots, and courses
- User dashboard with performance tracking
- Admin dashboard for content management
- Subscription and payment management
- Bot licensing and activation system
- Community and educational resources

## Technology Stack
- **Frontend**: Vue.js 3, Vue Router, Pinia, Axios
- **Backend**: Django, Django REST Framework, JWT Authentication
- **Database**: MySQL

## Project Structure
```
fintech-platform/
├── backend/               # Django backend
│   ├── api/               # API app for product and order management
│   ├── core/              # Core Django settings
│   ├── users/             # User authentication and management
│   ├── manage.py          # Django management script
│   ├── requirements.txt   # Python dependencies
│   └── venv/              # Python virtual environment
├── frontend/              # Vue.js frontend
│   ├── src/               # Source code
│   │   ├── assets/        # Static assets
│   │   ├── components/    # Vue components
│   │   ├── router/        # Vue Router configuration
│   │   ├── store/         # Pinia stores
│   │   ├── views/         # Vue views
│   │   ├── App.vue        # Main app component
│   │   └── main.js        # Entry point
│   ├── index.html         # HTML template
│   ├── package.json       # NPM dependencies
│   └── vite.config.js     # Vite configuration
└── README.md              # This file
```

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the database in `core/settings.py`

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/users/register/` - Register a new user
- `POST /api/users/login/` - Login user
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile
- `POST /api/users/change-password/` - Change password

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{slug}/` - Get product details
- `GET /api/categories/` - List all categories
- `GET /api/categories/{slug}/` - Get category details

### Orders
- `GET /api/orders/` - List user orders
- `POST /api/orders/create/` - Create a new order
- `GET /api/orders/{order_number}/` - Get order details

## Deployment
The application can be deployed to any hosting service that supports Django and Vue.js applications. For production deployment, make sure to:

1. Set `DEBUG = False` in Django settings
2. Configure proper database settings
3. Set up proper CORS headers
4. Build the Vue.js frontend with `npm run build`
5. Serve the static files from the Django application

## License
This project is proprietary and confidential.
