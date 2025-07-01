# URL Shortener

![Build Status]([https://github.com/n3rwus/url-shortener/workflows/Tests/badge.svg](https://github.com/n3rwus/url-shortener/workflows/Python-app/badge.svg))
![Tests](https://github.com/n3rwus/url-shortener/workflows/CI/badge.svg](https://github.com/n3rwus/url-shortener/workflows/Pylint/badge.svg))
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Flask Version](https://img.shields.io/badge/flask-2.0%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Code Coverage](https://codecov.io/gh/n3rwus/url-shortener/branch/main/graph/badge.svg)

A simple, fast, and secure URL shortener built with Flask. Transform long URLs into short, manageable links with analytics and custom aliases support.

## 🎯 Motivation

In today's digital world, sharing long URLs can be cumbersome and unprofessional. This project was born out of the need for a lightweight, self-hosted URL shortening service that prioritizes:

- **Privacy**: Your data stays under your control
- **Simplicity**: Clean, minimalist design focused on functionality
- **Performance**: Fast redirects with minimal overhead
- **Security**: Built-in protection against malicious URLs and abuse
- **Learning**: A practical project to explore Flask, REST APIs, and web security

## 📋 Description

This URL shortener provides a REST API built with Flask that allows users to:

- **Shorten URLs**: Convert long URLs into short, shareable links
- **Custom Aliases**: Create memorable short codes for your links
- **Analytics**: Track click counts and basic usage statistics
- **Bulk Operations**: Shorten multiple URLs at once
- **Expiration Control**: Set automatic expiration dates for links
- **Safe Browsing**: Automatic detection and blocking of malicious URLs

### Key Features

- 🚀 **Fast & Lightweight**: Minimal dependencies, maximum performance
- 🔒 **Security First**: Input validation, rate limiting, and malicious URL detection
- 📊 **Basic Analytics**: Click tracking and usage statistics
- 🎨 **Clean API**: RESTful endpoints with clear documentation
- 🐳 **Docker Ready**: Easy deployment with Docker support
- 🧪 **Well Tested**: Comprehensive test suite with high coverage
- 📱 **Mobile Friendly**: Responsive design for all devices

## 🛠️ Built With

- **Backend**: Python 3.8+, Flask 2.0+
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Validation**: Validators, URL parsing
- **Testing**: pytest, coverage
- **Security**: Rate limiting, input sanitization
- **Deployment**: Docker, GitHub Actions

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000` to start shortening URLs!

## 📈 Project Status

This is an active hobby project maintained in my spare time. While it's functional and secure, it's designed for learning and small-scale usage rather than enterprise deployment.

**Current Status**: ✅ Stable for personal/hobby use

## 🤝 Contributing

Contributions are welcome! Whether it's bug fixes, feature suggestions, or documentation improvements, feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for privacy-focused URL shortening
- Built as a learning project to explore Flask and web security
- Thanks to the open-source community for the amazing tools and libraries

---

⭐ If you find this project useful, please consider giving it a star!
