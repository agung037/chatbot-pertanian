"""
WSGI entry point for the application.
This file is used by production WSGI servers like Gunicorn.
"""

from app import create_app

# Create the application instance
application = create_app()

# For running directly
if __name__ == '__main__':
    application.run() 