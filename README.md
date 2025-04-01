# URL Shortener API (Django Version)

## Overview
The URL Shortener API is a high-performance service that allows users to shorten long URLs into compact, shareable links. It provides functionalities to expand shortened URLs, track usage statistics, and optimize performance using Redis caching.

## Features
- Shorten long URLs into concise links
- Retrieve the original URL from a shortened link
- Track analytics for URL usage (redirect count)
- Delete shortened URLs
- Redis caching for improved performance
- Django REST Framework for API development

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Caching**: Redis
- **Deployment**: Docker (optional)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/girivaswani/Url-Shortner.git
   cd Url-Shortener
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the environment variables in a `.env` file:
   ```ini
   DATABASE_URL=postgresql://user:password@localhost:5432/url_shortener
   REDIS_URL=redis://localhost:6379/0
   ```
5. Update Redis configuration in `settings.py`:
   ```python
   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/0",  # Replace with your Redis URL
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
               # You can add other options here, like password if needed
               # "PASSWORD": "your_redis_password",
           }
       }
   }
   ```

## Running the API
To start the Django development server:
```sh
python manage.py runserver
```
The API will be available at: `http://127.0.0.1:8000`

## API Endpoints
### 1. Shorten a URL
**POST /urls/**
- **Request:**
  ```json
  {
    "original_url": "https://example.com"
  }
  ```
- **Response:**
  ```json
  {
    "short_url": "http://127.0.0.1:8000/abc123",
    "redirect_count": 0
  }
  ```

### 2. Retrieve the Original URL
**GET /{short_code}**
- Redirects to the original URL if found, otherwise returns an error.



## Performance Metrics
Performance was measured with and without Redis caching:

| Operation          | Without Redis (Req/sec)    | With Redis (Req/sec)    |
|--------------------|----------------------------|-------------------------|
| Create Short URL   | 61.55                      | 55.43                   |
| Get Long URL       | 45.01                      | 228.51                  |

| Operation          | Without Redis (ms/request) | With Redis (ms/request) |
|--------------------|----------------------------|-------------------------|
| Create Short URL   | 162.47                     | 180.40                  |
| Get Long URL       | 223.0                      | 43.89                   |


- **Retrieving long URLs is significantly faster with Redis caching.**
- **URL creation performance is slightly affected due to Redis write operations.**

## Future Enhancements
- User authentication for managing shortened URLs
- Custom short codes
- Expiry dates for shortened URLs
- Advanced analytics (click tracking, referrer data)


## Contact
For any queries or contributions, feel free to reach out!

