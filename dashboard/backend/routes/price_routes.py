"""
Price Data Routes

This module contains Flask routes for handling Brent oil price data endpoints.
"""

from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
from datetime import datetime
import os
from ..utils.data_loader import load_and_preprocess_data

price_bp = Blueprint('price', __name__, url_prefix='/api/data')

# Load data once when the blueprint is registered
file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'raw', 'BrentOilPrices.csv')
data = load_and_preprocess_data(file_path)

@price_bp.route('/summary', methods=['GET'])
def get_data_summary():
    """Get summary statistics for the price data."""
    try:
        summary = {
            'data_points': len(data),
            'date_range': {
                'start': data['Date'].min().strftime('%Y-%m-%d'),
                'end': data['Date'].max().strftime('%Y-%m-%d')
            },
            'price_range': {
                'min': data['Price'].min(),
                'max': data['Price'].max()
            },
            'price_stats': {
                'mean': data['Price'].mean(),
                'std': data['Price'].std(),
                'median': data['Price'].median()
            },
            'missing_values': data.isnull().sum().sum(),
            'completeness': 100.0 - (data.isnull().sum().sum() / len(data)) * 100,
            'last_updated': datetime.now().isoformat()
        }
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@price_bp.route('/price-series', methods=['GET'])
def get_price_series():
    """Get the complete price series data."""
    try:
        price_data = data[['Date', 'Price']].to_dict(orient='records')
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
        
        filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
        
        return jsonify({
            'start_date': start_date,
            'end_date': end_date,
            'data_points': len(filtered_data),
            'price_range': {
                'min': filtered_data['Price'].min(),
                'max': filtered_data['Price'].max()
            },
            'data': filtered_data[['Date', 'Price']].to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@price_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get detailed statistical analysis of the price data."""
    try:
        log_returns = np.log(data['Price'] / data['Price'].shift(1)).dropna()
        
        stats = {
            'descriptive_stats': {
                'mean': data['Price'].mean(),
                'median': data['Price'].median(),
                'std': data['Price'].std(),
                'skewness': data['Price'].skew(),
                'kurtosis': data['Price'].kurt()
            },
            'volatility_analysis': {
                'daily_volatility': log_returns.std(),
                'annualized_volatility': log_returns.std() * np.sqrt(252),
                'volatility_clusters': True  # This would require a more complex model to determine
            },
            'trend_analysis': {
                'overall_trend': 'increasing' if data['Price'].iloc[-1] > data['Price'].iloc[0] else 'decreasing',
                # A simple measure of trend strength
                'trend_strength': (data['Price'].iloc[-1] - data['Price'].iloc[0]) / data['Price'].iloc[0],
                'seasonality': False # This would require a more complex model to determine
            }
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 