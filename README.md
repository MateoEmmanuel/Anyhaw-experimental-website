# Any-Haw Restaurant Management System

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Environment Setup:
- Create a `.env` file in `static/assets/localfile/restaurantsetting.env`
- Add required environment variables:
  - SECRET_KEY
  - EMAIL_ADDRESS
  - EMAIL_PASSWORD
  - DATABASE_URL

3. Database Setup:
- Configure MySQL database
- Update connection settings in dbconnection.py

4. Run the application:
```bash
python app.py
```

## Directory Structure
- `/backend` - Backend Python modules
- `/static` - Static files (CSS, JS, images)
- `/templates` - HTML templates
- `app.py` - Main application file

## Default Admin Credentials
- Username: admin
- Password: admin123

## Features
- User Authentication
- Menu Management
- Order Processing
- Kitchen Display System
- Cashier Interface
- Delivery Management 