"""
Flask API Routes Package

This package contains all the route modules for the Brent Change Point Analysis API.
"""

from .price_routes import price_bp
from .event_routes import event_bp
from .model_routes import model_bp

__all__ = ['price_bp', 'event_bp', 'model_bp'] 