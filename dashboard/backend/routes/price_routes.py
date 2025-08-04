"""
Price Data Routes

This module contains Flask routes for handling Brent oil price data endpoints.
"""

from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

price_bp = Blueprint('price', __name__, url_prefix='/api/data')

@price_bp.route('/summary', methods=['GET'])
def get_data_summary():
    """Get summary statistics for the price data."""
    try:
        # Mock data - in real implementation, load from processed data
        summary = {
            'data_points': 5000,
            'date_range': {
                'start': '2010-01-01',
                'end': '2024-01-01'
            },
            'price_range': {
                'min': 20.50,
                'max': 140.50
            },
            'price_stats': {
                'mean': 75.30,
                'std': 25.40,
                'median': 70.20
            },
            'missing_values': 0,
            'completeness': 100.0,
            'last_updated': datetime.now().isoformat()
        }
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@price_bp.route('/price-series', methods=['GET'])
def get_price_series():
    """Get the complete price series data."""
    try:
        # Mock data - in real implementation, load from processed data
        start_date = datetime(2020, 1, 1)
        dates = [start_date + timedelta(days=i) for i in range(100)]
        
        # Generate mock price data with some volatility
        np.random.seed(42)
        base_price = 70.0
        prices = []
        for i in range(100):
            # Add some trend and volatility
            trend = 0.1 * np.sin(i / 10)  # Cyclical trend
            noise = np.random.normal(0, 2)  # Random noise
            price = base_price + trend + noise
            prices.append(max(20, price))  # Ensure positive prices
        
        price_data = [
            {
                'date': date.strftime('%Y-%m-%d'),
                'price': round(price, 2)
            }
            for date, price in zip(dates, prices)
        ]
        
        return jsonify(price_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@price_bp.route('/price-range', methods=['GET'])
def get_price_range():
    """Get price data for a specific date range."""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'start_date and end_date parameters are required'}), 400
        
        # Mock implementation - filter data by date range
        # In real implementation, load and filter actual data
        
        return jsonify({
            'start_date': start_date,
            'end_date': end_date,
            'data_points': 100,
            'price_range': {
                'min': 65.20,
                'max': 85.40
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@price_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get detailed statistical analysis of the price data."""
    try:
        # Mock statistical analysis
        stats = {
            'descriptive_stats': {
                'mean': 75.30,
                'median': 70.20,
                'std': 25.40,
                'skewness': 0.15,
                'kurtosis': 2.8
            },
            'volatility_analysis': {
                'daily_volatility': 2.1,
                'annualized_volatility': 0.33,
                'volatility_clusters': True
            },
            'trend_analysis': {
                'overall_trend': 'increasing',
                'trend_strength': 0.65,
                'seasonality': True
            }
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 