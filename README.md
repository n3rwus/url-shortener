# URL Shortener

[//]: # (![Python app]&#40;https://github.com/n3rwus/url-shortener/workflows/Python-app/badge.svg&#41;)

[//]: # (![Tests]&#40;https://github.com/n3rwus/url-shortener/workflows/Pylint/badge.svg&#41;)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI Version](https://img.shields.io/badge/FastAPI-2.0%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
[![Codecov](https://codecov.io/github/n3rwus/url-shortener/branch/main/graph/badge.svg?token=RMAMAXML9G)](https://codecov.io/github/n3rwus/url-shortener)


A simple, fast, and secure URL shortener built with FastAPI. Transform long URLs into short, manageable links with analytics and intelligent security features.

## 🎯 Motivation

In today's digital world, sharing long URLs can be cumbersome and unprofessional. This project was born out of the need for a lightweight, self-hosted URL shortening service that prioritizes:

- **Privacy**: Your data stays under your control with self-hosted deployment
- **Security**: Real-time protection against malicious domains using trusted blacklists
- **Performance**: FastAPI's async capabilities ensure lightning-fast redirects
- **Simplicity**: Clean, minimalist API design focused on core functionality
- **Learning**: A practical project to explore modern Python web development with FastAPI
- **Production-Ready**: Docker deployment with secrets management and health monitoring

## 📋 Description

This URL shortener provides a modern REST API built with FastAPI that allows users to:

- **Shorten URLs**: Convert long URLs into short, shareable links with automatic collision handling
- **Security First**: Automatic malicious domain detection using CERT Poland's blacklist
- **Smart Caching**: In-memory caching for fast redirects and reduced database load
- **Analytics**: Track click counts and basic usage statistics
- **Expiration Control**: Set automatic expiration dates for links
- **Production Ready**: Docker deployment with PostgreSQL database support

### Key Features

- 🚀 **Fast & Lightweight**: Built on FastAPI for high performance with minimal overhead
- 🔒 **Security First**: Real-time domain validation against CERT Poland's malicious domain blacklist
- 📊 **Smart Analytics**: Click tracking with automatic increment on redirects
- 🎨 **Clean Architecture**: Repository pattern with service layer separation
- 🐳 **Production Ready**: Multi-stage Docker builds with secrets management
- 🧪 **Well Tested**: Comprehensive test suite with 32+ tests and high coverage
- 📖 **Auto Documentation**: Interactive API docs via FastAPI's built-in Swagger UI
- ⚡ **Intelligent Caching**: Timed cache decorators for optimal performance

## 🛠️ Built With

### Core Technologies
- **Backend**: Python 3.11+, FastAPI 0.115+
- **Database**: PostgreSQL with SQLAlchemy 2.0+ ORM
- **ASGI Server**: Uvicorn with asyncio support
- **Validation**: Pydantic models with automatic request/response validation

### Architecture & Design
- **Clean Architecture**: Repository pattern with service layer abstraction
- **Dependency Injection**: FastAPI's dependency system for clean testing
- **Environment Configuration**: Pydantic Settings with secrets management
- **Structured Logging**: Colorlog for development, structured logs for production

### Security & Performance
- **Domain Security**: Integration with CERT Poland's blacklist API
- **Caching**: Custom timed cache decorators for performance optimization
- **Input Validation**: URL scheme validation and domain checking
- **CORS**: Configurable cross-origin resource sharing

### DevOps & Deployment
- **Containerization**: Multi-stage Docker builds for optimized images
- **Secrets Management**: Docker secrets integration for sensitive configuration
- **Health Checks**: Built-in health endpoints for monitoring
- **Testing**: pytest with coverage, async testing support

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database
- Docker (optional, recommended for production)

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/n3rwus/url-shortener.git
cd url-shortener

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (copy .env.test for development)
cp .env.test .env

# Configure your database settings in .env:
# USER=your_db_user
# PASSWORD=your_db_password
# HOST=localhost
# PORT=5432
# DBNAME=url_shortener

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build the Docker image manually
docker build -t url-shortener .
docker run -p 8000:8000 url-shortener
```

### API Documentation

Once running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)
- **Health Check**: `http://localhost:8000/v1/health`

### Basic Usage

```bash
# Shorten a URL
curl -X POST "http://localhost:8000/urls" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/very/long/url"}'

# Access shortened URL (replace {short_code} with actual code)
curl -L "http://localhost:8000/{short_code}"
```

## 🔒 Security Features

This application implements several security measures to protect against malicious URLs and abuse:

### Domain Blacklist Integration
- **Real-time Validation**: Integration with CERT Poland's malicious domain blacklist
- **Automatic Updates**: Fetches the latest blacklist on each request with local backup
- **Graceful Fallback**: Uses cached local backup if remote service is unavailable

### Input Validation
- **URL Scheme Validation**: Only accepts `http` and `https` URLs
- **Domain Extraction**: Validates domains against known malicious sources
- **Request Validation**: Pydantic models ensure data integrity

### Error Handling
- **Graceful Degradation**: Service continues with local blacklist if remote fails
- **Detailed Logging**: Security events are logged for monitoring
- **User Feedback**: Clear error messages for rejected URLs

## 🏗️ Architecture

The application follows clean architecture principles with clear separation of concerns:

```
app/
├── core/           # Configuration, logging, caching
├── models/         # SQLAlchemy database models
├── schemas/        # Pydantic request/response models
├── repositories/   # Data access layer
├── service/        # Business logic layer
├── routes/         # API endpoint definitions
├── db/            # Database connection and session management
├── integration/   # External service integrations (blacklist)
└── utils/         # Utility functions
```

### Design Patterns
- **Repository Pattern**: Clean separation between business logic and data access
- **Dependency Injection**: FastAPI's dependency system for testable code
- **Service Layer**: Business logic encapsulation with clear interfaces
- **Configuration Management**: Environment-based configuration with secrets support

## 📈 Project Status

This is an active hobby project maintained in my spare time. While it's functional and secure, it's designed for learning and small-scale usage rather than enterprise deployment.

**Current Status**: ✅ Stable for personal/hobby use
**Test Coverage**: 32+ tests covering core functionality
**Performance**: Optimized with caching and async operations

## 🧪 Development & Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage report
python -m pytest --cov=app

# Run specific test file
python -m pytest test/test_url_service.py -v

# Run tests with detailed output
python -m pytest -v --tb=short
```

### Code Quality

```bash
# The project includes comprehensive testing:
# - Unit tests for all components
# - Integration tests for API endpoints
# - Mock testing for external dependencies
# - Async test support for FastAPI routes
```

### Development Workflow

1. **Setup Development Environment**:
   ```bash
   pip install -r requirements.txt
   cp .env.test .env  # Configure your local settings
   ```

2. **Run Application in Development Mode**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Test Your Changes**:
   ```bash
   python -m pytest test/
   ```

4. **Access API Documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Environment Configuration

The application supports flexible configuration through environment variables or Docker secrets:

```bash
# Database Configuration
USER=your_db_user
PASSWORD=your_db_password  
HOST=localhost
PORT=5432
DBNAME=url_shortener

# Application Settings
BASE_URL=http://localhost:8000
ENV=development  # Set to 'production' to disable docs
REDIS_URL=redis://localhost:6379  # Optional caching
```

## 🤝 Contributing

Contributions are welcome! Whether it's bug fixes, feature suggestions, or documentation improvements, feel free to open an issue or submit a pull request.

### Getting Started with Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run the test suite (`python -m pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for privacy-focused URL shortening services
- Built as a learning project to explore FastAPI, async Python, and clean architecture
- Thanks to [CERT Poland](https://www.cert.pl/) for providing the malicious domain blacklist
- FastAPI community for excellent documentation and framework design
- PostgreSQL and SQLAlchemy teams for robust database solutions
- Open-source community for the amazing tools and libraries that make this possible

---

⭐ If you find this project useful, please consider giving it a star!
