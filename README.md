### Rent Ease Backend

A simple and reliable API for property rental apps. Helps landlords manage properties and helps tenants find and book places to rent.



### What It Does

- Landlords can list and manage properties
- Tenants can browse and book properties  
- Handles property images and photos
- Sends email updates for bookings
- Admin tools to manage everything






## Features

- Property & booking management
- JWT authentication & authorization  
- Image upload with Cloudinary
- Email notifications via SendGrid
- Admin dashboard endpoints
- Real-time statistics

## Quick Start

### Prerequisites
- Python 3.10
- Pipenv


# Start server
python app.py

API Endpoints

### Properties


GET /properties - List all properties

POST /properties - Create new property

GET /properties/:id - Get property details

### Bookings

POST /bookings - Create booking request

GET /bookings?tenant_id=:id - User bookings

PUT /bookings/:id - Approve/reject booking

### Utilities

GET /api/health - Server status

GET /api/stats - System statistics

POST /api/upload - Image upload (JWT protected)

### Admin


GET /admin/users - User management

GET /admin/properties - All properties

GET /admin/bookings - All bookings



### Tech Stack


Backend: Flask, SQLAlchemy, JWT

Database: SQLite

Services: Cloudinary, SendGrid

Auth: JWT tokens



