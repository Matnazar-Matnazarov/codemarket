# CodeMarket - Professional Code Marketplace Platform

[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<div align="center">
  <img src="https://www.djangoproject.com/m/img/logos/django-logo-positive.png" alt="Django Logo" width="200"/>
  <h3>A modern marketplace for buying and selling code projects</h3>
</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## 🎯 Overview

CodeMarket is a comprehensive Django-based web application that serves as a marketplace for developers to buy and sell code projects. The platform provides a secure, user-friendly environment for code transactions with features like user authentication, project management, and payment processing.

### Key Features:
- **User Authentication**: Secure login with email/password and OAuth (Google, GitHub)
- **Project Management**: Create, edit, and manage code projects
- **Marketplace**: Browse and purchase code projects
- **Payment System**: Integrated payment processing
- **Admin Panel**: Comprehensive admin interface with Jazzmin theme
- **API**: RESTful API for mobile and third-party integrations
- **Multi-language Support**: English, Uzbek, and Russian languages

## 🚀 Features

### Core Functionality
- ✅ User registration and authentication
- ✅ OAuth integration (Google, GitHub)
- ✅ Project creation and management
- ✅ Project marketplace
- ✅ Payment processing
- ✅ User profiles and settings
- ✅ Admin dashboard
- ✅ REST API endpoints
- ✅ Email notifications
- ✅ Multi-language support

### Technical Features
- ✅ Django 5.x with modern practices
- ✅ PostgreSQL database
- ✅ Redis for caching
- ✅ JWT authentication
- ✅ Swagger API documentation
- ✅ Tailwind CSS for styling
- ✅ Responsive design
- ✅ Security best practices

## 🛠 Technology Stack

### Backend
- **Framework**: Django 5.x
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT, OAuth2 (Google, GitHub)
- **API**: Django REST Framework
- **Documentation**: Swagger/OpenAPI (drf-yasg)
- **Admin**: Jazzmin

### Frontend
- **CSS Framework**: Tailwind CSS
- **JavaScript**: Vanilla JS
- **Templates**: Django Templates
- **Admin Theme**: Jazzmin
- **Rich Text Editor**: CKEditor 5

### Development Tools
- **Package Manager**: pip
- **Environment**: environs
- **Code Quality**: Black, autopep8
- **Version Control**: Git

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 12+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis** - [Download Redis](https://redis.io/download)
- **Git** - [Download Git](https://git-scm.com/downloads)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Matnazar-Matnazarov/codemarket.git
cd codemarket
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```


### 5. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/codemarket

# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,*

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
```

### 6. Database Setup

```bash
# Create PostgreSQL database
createdb codemarket

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```



### 8. Static Files Setup

```bash
# Collect static files
python manage.py collectstatic --noinput

# Create media directory (if not exists)
mkdir -p media
```

## ⚙️ Configuration

### Database Configuration

The project uses PostgreSQL by default. Update your database settings in `config/settings.py` or use the `DATABASE_URL` environment variable.

### Email Configuration

Configure your email settings in the `.env` file:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### OAuth Configuration

#### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`

#### GitHub OAuth
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create a new OAuth App
3. Set callback URL: `http://localhost:8000/accounts/github/login/callback/`

## 🎮 Usage

### Running the Development Server

```bash
# Start the development server
python manage.py runserver

# Access the application
# Open http://127.0.0.1:8000/ in your browser
```

### Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

### API Endpoints

The project includes a comprehensive REST API. Access the API documentation at:
- **Swagger UI**: `http://127.0.0.1:8000/api/swagger/`