"""
Flask Backend for Brent Change Point Analysis Dashboard

This module provides the main Flask application and API endpoints
for serving change point analysis results to the frontend.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from modeling.model_runner import ModelRunner
from modeling.diagnostics import ModelDiagnostics, ChangePointVisualizer

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Global variables for loaded data and models
data = None
model_results = None
model_runner = None

def load_data():
    """Load data and model results."""
    global data, model_results, model_runner
    
    try:
        # Load processed data
        data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'events_aligned.csv')
        data = pd.read_csv(data_path)
        data['Date'] = pd.to_datetime(data['Date'])
        
        # Load model results if available
        results_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'model_results.pkl')
        if os.path.exists(results_path):
            with open(results_path, 'rb') as f:
                model_results = pickle.load(f)
        
        # Initialize model runner
        model_runner = ModelRunner(data_path)
        
        print("Data and models loaded successfully")
        return True
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'data_loaded': data is not None,
        'model_loaded': model_results is not None
    })

@app.route('/api/data/summary', methods=['GET'])
def get_data_summary():
    """Get summary statistics of the data."""
    if data is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    summary = {
        'total_observations': len(data),
        'date_range': {
            'start': data['Date'].min().isoformat(),
            'end': data['Date'].max().isoformat()
        },
        'columns': list(data.columns),
        'missing_values': data.isnull().sum().to_dict(),
        'price_stats': {
            'mean': float(data['Close'].mean()),
            'std': float(data['Close'].std()),
            'min': float(data['Close'].min()),
            'max': float(data['Close'].max())
        },
        'returns_stats': {
            'mean': float(data['Returns'].mean()),
            'std': float(data['Returns'].std()),
            'min': float(data['Returns'].min()),
            'max': float(data['Returns'].max())
        }
    }
    
    return jsonify(summary)

@app.route('/api/data/price-series', methods=['GET'])
def get_price_series():
    """Get price time series data."""
    if data is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Get date range from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    filtered_data = data.copy()
    
    if start_date:
        filtered_data = filtered_data[filtered_data['Date'] >= start_date]
    if end_date:
        filtered_data = filtered_data[filtered_data['Date'] <= end_date]
    
    # Convert to JSON-serializable format
    price_series = {
        'dates': filtered_data['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'prices': filtered_data['Close'].tolist(),
        'returns': filtered_data['Returns'].tolist(),
        'volatility': filtered_data['Volatility_30d'].tolist()
    }
    
    return jsonify(price_series)

@app.route('/api/events/summary', methods=['GET'])
def get_events_summary():
    """Get summary of event data."""
    if data is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    event_features = ['Event_Count_30d', 'High_Impact_Event_30d', 'War_Event_30d', 
                     'OPEC_Event_30d', 'Crisis_Event_30d', 'Days_Since_Last_Event']
    
    event_summary = {}
    for feature in event_features:
        if feature in data.columns:
            event_summary[feature] = {
                'mean': float(data[feature].mean()),
                'std': float(data[feature].std()),
                'max': float(data[feature].max()),
                'total_events': int(data[feature].sum())
            }
    
    return jsonify(event_summary)

@app.route('/api/model/status', methods=['GET'])
def get_model_status():
    """Get status of fitted models."""
    if model_results is None:
        return jsonify({
            'models_fitted': False,
            'message': 'No models have been fitted yet'
        })
    
    status = {
        'models_fitted': True,
        'basic_model': 'basic_model' in model_results,
        'event_model': 'event_model' in model_results
    }
    
    if 'basic_model' in model_results and 'event_model' in model_results:
        basic_waic = model_results['basic_model']['waic'].waic
        event_waic = model_results['event_model']['waic'].waic
        status['waic_comparison'] = {
            'basic_waic': float(basic_waic),
            'event_waic': float(event_waic),
            'preferred_model': 'event_model' if event_waic < basic_waic else 'basic_model'
        }
    
    return jsonify(status)

@app.route('/api/model/changepoints', methods=['GET'])
def get_changepoints():
    """Get detected change points."""
    if model_results is None or 'event_model' not in model_results:
        return jsonify({'error': 'Event model not fitted'}), 500
    
    trace = model_results['event_model']['trace']
    
    # Extract change points
    changepoints_posterior = trace.posterior['changepoints_sorted'].values
    changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
    changepoints_hdi = trace.posterior['changepoints_sorted'].quantile([0.025, 0.975], dim=('chain', 'draw'))
    
    changepoints = []
    for i, mean_cp in enumerate(changepoints_mean):
        cp_date = data.iloc[int(mean_cp)]['Date']
        changepoints.append({
            'id': i + 1,
            'date': cp_date.strftime('%Y-%m-%d'),
            'time_index': int(mean_cp),
            'hdi_lower': int(changepoints_hdi.sel(quantile=0.025).values[i]),
            'hdi_upper': int(changepoints_hdi.sel(quantile=0.975).values[i])
        })
    
    return jsonify({'changepoints': changepoints})

@app.route('/api/model/event-coefficients', methods=['GET'])
def get_event_coefficients():
    """Get event coefficient estimates."""
    if model_results is None or 'event_model' not in model_results:
        return jsonify({'error': 'Event model not fitted'}), 500
    
    trace = model_results['event_model']['trace']
    
    # Extract event coefficients
    event_coeff_posterior = trace.posterior['event_coefficients'].values
    event_coeff_mean = event_coeff_posterior.mean(axis=(0, 1))
    event_coeff_hdi = trace.posterior['event_coefficients'].quantile([0.025, 0.975], dim=('chain', 'draw'))
    
    event_names = ['Event_Count_30d', 'High_Impact_Event_30d', 'War_Event_30d', 
                  'OPEC_Event_30d', 'Crisis_Event_30d', 'Days_Since_Last_Event']
    
    coefficients = []
    for i, name in enumerate(event_names):
        coefficients.append({
            'feature': name,
            'mean': float(event_coeff_mean[i]),
            'hdi_lower': float(event_coeff_hdi.sel(quantile=0.025).values[i]),
            'hdi_upper': float(event_coeff_hdi.sel(quantile=0.975).values[i]),
            'significant': (event_coeff_hdi.sel(quantile=0.025).values[i] > 0 or 
                          event_coeff_hdi.sel(quantile=0.975).values[i] < 0)
        })
    
    return jsonify({'coefficients': coefficients})

@app.route('/api/model/segments', methods=['GET'])
def get_segments():
    """Get segment characteristics."""
    if model_results is None or 'event_model' not in model_results:
        return jsonify({'error': 'Event model not fitted'}), 500
    
    trace = model_results['event_model']['trace']
    
    # Extract segment parameters
    segment_intercepts_posterior = trace.posterior['segment_intercepts'].values
    segment_sigmas_posterior = trace.posterior['segment_sigmas'].values
    
    segment_intercepts_mean = segment_intercepts_posterior.mean(axis=(0, 1))
    segment_sigmas_mean = segment_sigmas_posterior.mean(axis=(0, 1))
    
    # Get change points for segment boundaries
    changepoints_posterior = trace.posterior['changepoints_sorted'].values
    changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
    
    segments = []
    y = data['Returns'].values
    
    for i in range(len(changepoints_mean) + 1):
        start_idx = int(changepoints_mean[i-1]) if i > 0 else 0
        end_idx = int(changepoints_mean[i]) if i < len(changepoints_mean) else len(y)
        
        start_date = data.iloc[start_idx]['Date']
        end_date = data.iloc[end_idx-1]['Date']
        
        segment_returns = y[start_idx:end_idx]
        
        segments.append({
            'id': i + 1,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'duration_days': end_idx - start_idx,
            'mean_return': float(segment_returns.mean()),
            'std_return': float(segment_returns.std()),
            'model_intercept': float(segment_intercepts_mean[i]),
            'model_sigma': float(segment_sigmas_mean[i])
        })
    
    return jsonify({'segments': segments})

@app.route('/api/model/run', methods=['POST'])
def run_model():
    """Run the change point model."""
    if model_runner is None:
        return jsonify({'error': 'Model runner not initialized'}), 500
    
    try:
        # Get parameters from request
        params = request.get_json() or {}
        n_changepoints = params.get('n_changepoints', 5)
        samples = params.get('samples', 1000)  # Reduced for faster response
        tune = params.get('tune', 500)
        chains = params.get('chains', 2)
        
        # Run models
        print("Running basic model...")
        basic_trace = model_runner.run_basic_model(n_changepoints, samples, tune, chains)
        
        print("Running event model...")
        event_trace = model_runner.run_event_model(n_changepoints, samples, tune, chains)
        
        # Compare models
        comparison = model_runner.compare_models()
        
        # Save results
        output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'model_results.pkl')
        model_runner.save_results(output_path)
        
        return jsonify({
            'status': 'success',
            'message': 'Models fitted successfully',
            'comparison': comparison
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/correlation', methods=['GET'])
def get_correlation_analysis():
    """Get correlation analysis between events and returns."""
    if data is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    event_features = ['Event_Count_30d', 'High_Impact_Event_30d', 'War_Event_30d', 
                     'OPEC_Event_30d', 'Crisis_Event_30d', 'Days_Since_Last_Event']
    
    correlations = {}
    for feature in event_features:
        if feature in data.columns:
            corr = data['Returns'].corr(data[feature])
            correlations[feature] = {
                'correlation': float(corr),
                'abs_correlation': float(abs(corr)),
                'significant': abs(corr) > 0.05
            }
    
    return jsonify({'correlations': correlations})

if __name__ == '__main__':
    # Load data on startup
    if load_data():
        print("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to load data. Exiting.")
        exit(1) 