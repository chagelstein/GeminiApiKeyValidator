# Gemini API Key Tester

## Overview

This is a Flask-based web application designed to test and validate Google Gemini API keys. The application provides a user-friendly interface for developers to verify their API key connectivity and get detailed diagnostic information about their Gemini API access.

## System Architecture

### Frontend Architecture
- **Framework**: HTML5 with Bootstrap 5 (dark theme)
- **Styling**: Custom CSS with Bootstrap integration
- **JavaScript**: Vanilla JavaScript for client-side interactions
- **UI Components**: Form-based interface with password toggle, loading states, and flash messages

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Structure**: Simple MVC pattern with routes and templates
- **Entry Point**: `main.py` imports the Flask app from `app.py`
- **Session Management**: Flask sessions with configurable secret key

### API Integration
- **Primary Service**: Google Generative AI (Gemini)
- **Purpose**: API key validation and model information retrieval
- **Configuration**: Runtime API key configuration through web interface

## Key Components

### Core Application Files
- `app.py`: Main Flask application with routes and API testing logic
- `main.py`: Application entry point for deployment
- `templates/index.html`: Main user interface template
- `static/css/style.css`: Custom styling and theme enhancements
- `static/js/main.js`: Client-side JavaScript functionality

### Configuration Files
- `pyproject.toml`: Python project dependencies and metadata
- `.replit`: Replit environment configuration with deployment settings
- `uv.lock`: Dependency lock file for reproducible builds

### Key Features
1. **API Key Validation**: Tests provided API keys against Gemini services
2. **Model Discovery**: Lists available Gemini models for the API key
3. **Secure Input**: Password-style input with toggle visibility
4. **Error Handling**: Comprehensive error reporting and user feedback
5. **Responsive Design**: Mobile-friendly Bootstrap interface

## Data Flow

1. **User Input**: User enters API key through web form
2. **Validation**: Basic client-side validation (length checks)
3. **API Testing**: Server-side Gemini API connectivity testing
4. **Model Enumeration**: Retrieval of available models for the API key
5. **Results Display**: Comprehensive test results with success/failure indicators
6. **Feedback**: Flash messages for user notifications

## External Dependencies

### Python Packages
- `flask`: Web framework for the application
- `google-generativeai`: Official Google Gemini API client
- `gunicorn`: WSGI HTTP server for production deployment
- `psycopg2-binary`: PostgreSQL adapter (for potential future database features)
- `flask-sqlalchemy`: SQL toolkit (not currently used but available)
- `email-validator`: Email validation utilities

### Frontend Dependencies
- Bootstrap 5 (CDN): UI framework and styling
- Font Awesome 6 (CDN): Icon library
- Custom Bootstrap theme optimized for Replit Agent

### Infrastructure
- PostgreSQL: Available through Nix packages (not currently used)
- OpenSSL: Security libraries for HTTPS connections

## Deployment Strategy

### Environment
- **Platform**: Replit with Nix environment
- **Python Version**: 3.11
- **Deployment Target**: Autoscale configuration

### Production Setup
- **WSGI Server**: Gunicorn with hot reload capabilities
- **Binding**: 0.0.0.0:5000 for external access
- **Process Management**: Port reuse and reload on changes
- **Environment Variables**: Session secret configuration

### Development Workflow
- **Run Configuration**: Parallel workflow execution
- **Hot Reload**: Automatic application restart on code changes
- **Port Management**: Automatic port waiting and binding

## Changelog

```
Changelog:
- June 14, 2025. Initial setup
- June 14, 2025. Enhanced API testing to list all available models with detailed information including supported methods, token limits, and descriptions. Added collapsible accordion interface to display models in an organized manner.
- June 14, 2025. Implemented intelligent model selection for API testing using popularity-based priority (gemini-1.5-pro, gemini-1.5-flash, gemini-pro, etc.). Added visual indicators for popular/recommended models in the interface.
- June 17, 2025. Redesigned model display to show only top 10 most recent models in descending order with total model count information. Improved user experience by focusing on latest available models.
```

## Backup & Safety

### File Protection
- All files are automatically saved in Replit's cloud infrastructure
- Project persists across sessions and devices
- No manual saving required

### Recommended Backup Options
1. **Git Integration**: Connect to GitHub for version control and external backup
2. **Download ZIP**: Use Replit's download feature for local backups
3. **Project Forking**: Create duplicate copies within Replit

### Project Status
- Application successfully deployed and tested
- Rate limiting issues resolved with gemini-1.5-flash prioritization
- All core functionality working as expected

## User Preferences

```
Preferred communication style: Simple, everyday language.
```