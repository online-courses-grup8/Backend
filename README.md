# Edutics Backend

## Overview

Edutics is a production-ready online learning platform backend built with Django REST Framework. The platform allows users to register, purchase courses, track their learning progress, participate in events, read blog content, and manage their profiles.

The project follows a Service-Selector architecture that separates business logic from database access, resulting in a scalable, maintainable, and highly testable codebase.

Media files are stored in Azure Blob Storage, authentication is handled through a custom JWT implementation, and deployment is designed around Docker and Azure services.

---

## Features

* Custom JWT Authentication (Access & Refresh Tokens)
* User Registration and Profile Management
* Course Catalog and Curriculum Management
* Course Purchase and Checkout System
* Lesson Completion Tracking
* Learning Progress Monitoring
* Event Registration System
* Instructor Management
* Blog Management System
* Course Recommendation Engine
* Newsletter Subscription
* Contact Form Management
* FAQ Management
* Platform Statistics
* Azure Blob Storage Integration
* Dockerized Deployment
* Azure-Based Infrastructure
* Unit Tested Architecture

---

## Architecture

The project follows the Service-Selector Pattern.

```text
Request
   ↓
View
   ↓
Selector / Service
   ↓
Model
   ↓
Response
```

### Layer Responsibilities

| Layer       | Responsibility                     |
| ----------- | ---------------------------------- |
| Views       | HTTP request/response handling     |
| Serializers | Validation and data transformation |
| Selectors   | Database queries                   |
| Services    | Business logic                     |
| Models      | Data persistence                   |

### Example Flow

```python
# views.py

class CourseListView(APIView):
    def get(self, request):
        courses = get_published_courses()
        serializer = CourseListSerializer(courses, many=True)

        return Response({
            "status": 200,
            "payload": serializer.data,
            "errorMessage": None
        })
```

```python
# selectors.py

def get_published_courses():
    return Course.objects.filter(
        is_published=True
    )
```

This approach keeps database access isolated within selectors while business rules remain inside services, making the application easier to test and maintain.

---

## Tech Stack

### Backend

* Django 6
* Django REST Framework
* PostgreSQL

### Authentication

* Custom JWT Authentication
* PyJWT

### Cloud Services

* Azure Blob Storage
* Azure Database for PostgreSQL

### DevOps

* Docker
* Azure Pipelines

### Testing

* Django SimpleTestCase
* unittest.mock.MagicMock

---

## Project Structure

```text
edutics/
│
├── users/
│   ├── serializers/
│   ├── selectors/
│   ├── services/
│   ├── views/
│   ├── tests/
│   └── models.py
│
├── courses/
│   ├── serializers/
│   ├── selectors/
│   ├── services/
│   ├── views/
│   ├── tests/
│   └── models.py
│
├── events/
├── payments/
├── blog/
├── core/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── requirements.txt
├── Dockerfile
├── manage.py
└── README.md
```

---

## Authentication Flow

Edutics uses a custom JWT authentication mechanism.

```text
Register
    ↓
Login
    ↓
Access Token (60 Minutes)
Refresh Token (7 Days)
    ↓
Protected Endpoints
    ↓
Refresh Access Token
```

Authenticated requests must include the access token:

```http
Authorization: Bearer <access_token>
```

---

## Media Storage

All uploaded media files are stored in Azure Blob Storage.

### Upload Flow

```text
Base64 Image
      ↓
Serializer Validation
      ↓
Azure Blob Storage
      ↓
Public URL Generation
      ↓
Database Storage
```

Supported uploads include:

* User profile images
* Course thumbnails
* Instructor photos
* Blog thumbnails

---

## Installation

### Requirements

* Python 3.12+
* PostgreSQL
* Azure Blob Storage Account

### Clone Repository

```bash
git clone <repository-url>
cd edutics
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment File

```bash
cp .env.example .env
```

### Environment Variables

```env
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

# Azure Blob Storage
AZURE_ACCOUNT_NAME=your_account_name
AZURE_ACCOUNT_KEY=your_account_key
AZURE_CONTAINER=media

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7
```

### Apply Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

---

## API Endpoints

All endpoints are prefixed with:

```text
/api/v1/
```

### Authentication

| Method | Endpoint        |
| ------ | --------------- |
| POST   | /auth/register/ |
| POST   | /auth/login/    |
| POST   | /auth/refresh/  |

### Profile

| Method | Endpoint                      |
| ------ | ----------------------------- |
| GET    | /profile/                     |
| PATCH  | /profile/update/              |
| PUT    | /profile/change-password/     |
| DELETE | /profile/delete/              |
| GET    | /profile/my-courses/          |
| GET    | /profile/my-events/           |
| GET    | /profile/recommended-courses/ |
| GET    | /profile/my-instructors/      |

### Courses

| Method | Endpoint                    |
| ------ | --------------------------- |
| GET    | /courses/                   |
| GET    | /courses/<slug>/overview/   |
| GET    | /courses/<slug>/curriculum/ |
| GET    | /courses/<slug>/reviews/    |
| POST   | /courses/<slug>/comments/   |

### Categories

| Method | Endpoint     |
| ------ | ------------ |
| GET    | /categories/ |

### Instructors

| Method | Endpoint             |
| ------ | -------------------- |
| GET    | /instructors/        |
| GET    | /instructors/<slug>/ |

### Events

| Method | Endpoint                 |
| ------ | ------------------------ |
| GET    | /events/                 |
| GET    | /events/upcoming/        |
| GET    | /events/<slug>/          |
| POST   | /events/<slug>/register/ |

### Payments

| Method | Endpoint           |
| ------ | ------------------ |
| GET    | /cart/             |
| POST   | /cart/add/         |
| DELETE | /cart/remove/<id>/ |
| POST   | /cart/sync/        |
| POST   | /checkout/         |

### Blog

| Method | Endpoint |
| ------ | -------- |
| GET    | /blog/   |

### Core

| Method | Endpoint     |
| ------ | ------------ |
| GET    | /faqs/       |
| POST   | /contact/    |
| POST   | /newsletter/ |
| GET    | /stats/      |

---

## API Design Principles

The API follows a consistent response structure across all endpoints.

### Success Response

```json
{
    "status": 200,
    "payload": {},
    "errorMessage": null
}
```

### Error Response

```json
{
    "status": 400,
    "payload": null,
    "errorMessage": "Validation failed"
}
```

### Paginated Response

```json
{
    "status": 200,
    "payload": {
        "count": 10,
        "next": "http://...",
        "previous": null,
        "results": []
    },
    "errorMessage": null
}
```

Benefits:

* Consistent frontend integration
* Simplified error handling
* Predictable API behavior

---

## Testing Strategy

The project emphasizes fast and isolated unit testing.

### Principles

* No database dependency
* Extensive use of SimpleTestCase
* Mocked services and selectors
* Serializer validation testing
* Business logic verification

### Run All Tests

```bash
python manage.py test
```

### Run Specific App Tests

```bash
python manage.py test users
python manage.py test courses
python manage.py test payments
python manage.py test events
```

---

## CI/CD Pipeline

The project uses Azure Pipelines for continuous integration and deployment.

```text
Push to Repository
        ↓
Azure Pipeline Trigger
        ↓
Install Dependencies
        ↓
Run Unit Tests
        ↓
Build Docker Image
        ↓
Deployment Validation
        ↓
Deploy to Azure
```

Pipeline stages include:

* Dependency installation
* Automated testing
* Docker image creation
* Deployment verification

---

## Docker

### Build Image

```bash
docker build -t edutics .
```

### Run Container

```bash
docker run -p 8000:8000 edutics
```

---

## Future Improvements

Planned enhancements:

* Stripe Integration
* Course Certificates
* Wishlist System
* Advanced Search & Filtering
* Multi-language Support
* Instructor Dashboard
* Analytics Dashboard
* Swagger/OpenAPI Documentation
* Redis Caching
* Celery Background Tasks
* Email Notification System

---

## Contributing

1. Create a feature branch

```bash
git checkout -b feature/new-feature
```

2. Commit your changes

```bash
git commit -m "feat: add new feature"
```

3. Push the branch

```bash
git push origin feature/new-feature
```

4. Open a Pull Request

---

## License

This project is intended for educational and portfolio purposes.
All rights reserved.
