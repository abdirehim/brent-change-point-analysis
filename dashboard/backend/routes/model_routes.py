"""
Model Routes

This module contains Flask routes for handling Bayesian model endpoints and analysis results.
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import os
import pickle
import arviz as az

# Import ModelRunner and ModelDiagnostics for data preparation and diagnostics
from modeling.model_runner import ModelRunner
from modeling.diagnostics import ModelDiagnostics

model_bp = Blueprint('model', __name__, url_prefix='/api/model')

# Global variables for loaded data and models
model_results = None
data = None
model_runner_instance = None

def load_model_data():
    """Load model results and data for the API."""
    global model_results, data, model_runner_instance
    
    results_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'processed', 'model_results.pkl')
    data_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'processed', 'events_aligned.csv')

    try:
        if os.path.exists(results_path):
            with open(results_path, 'rb') as f:
                model_results = pickle.load(f)
            print("Model results loaded successfully.")
        else:
            print("Model results PKL not found. Models need to be run.")

        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            data['Date'] = pd.to_datetime(data['Date'])
            print("Aligned data loaded successfully.")
        else:
            print("Aligned data CSV not found.")

        # Initialize ModelRunner for data preparation and model access
        model_runner_instance = ModelRunner(data_path)

    except Exception as e:
        print(f"Error loading model data: {e}")

# Load data when the blueprint is initialized
load_model_data()

@model_bp.route('/status', methods=['GET'])
def get_model_status():
    """Get the current status of the Bayesian model."""
    if model_results is None:
        return jsonify({
            'models_fitted': False,
            'message': 'No models have been fitted yet or results not loaded.'
        })
    
    status = {
        'models_fitted': True,
        'basic_model_fitted': 'basic_model' in model_results,
        'event_model_fitted': 'event_model' in model_results,
        'last_run': datetime.now().isoformat(), # Placeholder, ideally from model_results metadata
        'model_version': '1.0.0' # Placeholder
    }
    
    if 'basic_model' in model_results and 'event_model' in model_results:
        basic_waic = model_results['basic_model']['waic'].waic
        event_waic = model_results['event_model']['waic'].waic
        status['waic_comparison'] = {
            'basic_waic': float(basic_waic),
            'event_waic': float(event_waic),
            'preferred_model': 'event_model' if event_waic < basic_waic else 'basic_model'
        }

        # Add convergence info if available
        if 'trace' in model_results['event_model']:
            event_trace = model_results['event_model']['trace']
            rhat_max = az.rhat(event_trace).max().item() if not az.rhat(event_trace).empty else 'N/A'
            ess_min = az.ess(event_trace).min().item() if not az.ess(event_trace).empty else 'N/A'
            status['convergence'] = {
                'r_hat_max': rhat_max,
                'effective_sample_size_min': ess_min,
                'is_converged': rhat_max < 1.05 if isinstance(rhat_max, (int, float)) else False # Common threshold
            }
    
    return jsonify(status)

@model_bp.route('/changepoints', methods=['GET'])
def get_change_points():
    """Get detected change points from the Bayesian model."""
    if model_results is None or 'event_model' not in model_results or 'trace' not in model_results['event_model']:
        return jsonify({'error': 'Event model not fitted or results not loaded.'}), 500
    
    event_trace = model_results['event_model']['trace']
    
    # Extract change points
    changepoints_posterior = event_trace.posterior['changepoints_sorted'].values
    changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
    changepoints_hdi = az.hdi(event_trace, var_names=['changepoints_sorted'])
    
    changepoints = []
    for i, mean_cp_idx in enumerate(changepoints_mean):
        # Ensure index is within bounds
        cp_idx = int(round(mean_cp_idx))
        if cp_idx < 0 or cp_idx >= len(data):
            continue # Skip if index is out of bounds

        cp_date = data.iloc[cp_idx]['Date']
        
        # HDI values are also indices, need to convert to dates
        hdi_lower_idx = int(round(changepoints_hdi['changepoints_sorted'].sel(changepoints_sorted_dim_0=i).values[0]))
        hdi_upper_idx = int(round(changepoints_hdi['changepoints_sorted'].sel(changepoints_sorted_dim_0=i).values[1]))

        hdi_lower_date = data.iloc[max(0, hdi_lower_idx)]['Date']
        hdi_upper_date = data.iloc[min(len(data)-1, hdi_upper_idx)]['Date']

        changepoints.append({
            'id': i + 1,
            'date': cp_date.strftime('%Y-%m-%d'),
            'time_index': cp_idx,
            'hdi_lower_date': hdi_lower_date.strftime('%Y-%m-%d'),
            'hdi_upper_date': hdi_upper_date.strftime('%Y-%m-%d'),
            'hdi_lower_index': hdi_lower_idx,
            'hdi_upper_index': hdi_upper_idx
        })
    
    return jsonify({'changepoints': changepoints})

@model_bp.route('/event-coefficients', methods=['GET'])
def get_event_coefficients():
    """Get event impact coefficients from the Bayesian model."""
    if model_results is None or 'event_model' not in model_results or 'trace' not in model_results['event_model']:
        return jsonify({'error': 'Event model not fitted or results not loaded.'}), 500
    
    event_trace = model_results['event_model']['trace']
    
    # Extract event coefficients
    event_coeff_posterior = event_trace.posterior['event_coefficients'].values
    event_coeff_mean = event_coeff_posterior.mean(axis=(0, 1))
    event_coeff_hdi = az.hdi(event_trace, var_names=['event_coefficients'])
    
    event_names = model_runner_instance.event_cols # Get actual event column names from ModelRunner
    
    coefficients = []
    for i, name in enumerate(event_names):
        # Ensure HDI values are scalars before converting to float
        hdi_lower = event_coeff_hdi['event_coefficients'].sel(event_coefficients_dim_0=i).values[0]
        hdi_upper = event_coeff_hdi['event_coefficients'].sel(event_coefficients_dim_0=i).values[1]

        coefficients.append({
            'feature': name,
            'mean': float(event_coeff_mean[i]),
            'hdi_lower': float(hdi_lower),
            'hdi_upper': float(hdi_upper),
            'significant': (hdi_lower > 0 or hdi_upper < 0) # Check if 0 is outside HDI
        })
    
    return jsonify({'coefficients': coefficients})

@model_bp.route('/segments', methods=['GET'])
def get_segments():
    """Get segment characteristics from the Bayesian model."""
    if model_results is None or 'event_model' not in model_results or 'trace' not in model_results['event_model']:
        return jsonify({'error': 'Event model not fitted or results not loaded.'}), 500
    
    event_trace = model_results['event_model']['trace']
    
    # Extract segment parameters
    segment_intercepts_posterior = event_trace.posterior['segment_intercepts'].values
    segment_sigmas_posterior = event_trace.posterior['segment_sigmas'].values
    
    segment_intercepts_mean = segment_intercepts_posterior.mean(axis=(0, 1))
    segment_sigmas_mean = segment_sigmas_posterior.mean(axis=(0, 1))
    
    # Get change points for segment boundaries
    changepoints_posterior = event_trace.posterior['changepoints_sorted'].values
    changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
    
    segments = []
    y = model_runner_instance.prepare_data()[0] # Get the target variable (log_return)
    
    # Add initial segment (before first change point)
    start_idx = 0
    end_idx = int(round(changepoints_mean[0])) if len(changepoints_mean) > 0 else len(y)
    
    start_date = data.iloc[start_idx]['Date']
    end_date = data.iloc[end_idx - 1]['Date'] if end_idx > 0 else start_date # Handle case with no data

    segments.append({
        'id': 0, # Segment before first CP
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'duration_days': (end_date - start_date).days,
        'mean_log_return': float(segment_intercepts_mean[0]),
        'volatility': float(segment_sigmas_mean[0])
    })

    # Add segments between change points
    for i in range(len(changepoints_mean)):
        start_idx = int(round(changepoints_mean[i]))
        end_idx = int(round(changepoints_mean[i+1])) if i+1 < len(changepoints_mean) else len(y)
        
        start_date = data.iloc[start_idx]['Date']
        end_date = data.iloc[end_idx - 1]['Date'] if end_idx > 0 else start_date

        segments.append({
            'id': i + 1,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'duration_days': (end_date - start_date).days,
            'mean_log_return': float(segment_intercepts_mean[i+1]),
            'volatility': float(segment_sigmas_mean[i+1])
        })
    
    return jsonify({'segments': segments})

@model_bp.route('/run', methods=['POST'])
def run_model():
    """Run the Bayesian change point analysis model."""
    global model_results, data, model_runner_instance

    if model_runner_instance is None:
        load_model_data() # Try to load data if not already loaded
        if model_runner_instance is None:
            return jsonify({'error': 'Model runner not initialized. Data might be missing.'}), 500

    try:
        params = request.get_json() or {}
        n_changepoints = params.get('n_changepoints', 5)
        samples = params.get('samples', 1000)  # Reduced for faster response
        tune = params.get('tune', 500)
        chains = params.get('chains', 2)
        
        print("Running basic model...")
        model_runner_instance.run_basic_model(n_changepoints, samples, tune, chains)
        
        print("Running event model...")
        model_runner_instance.run_event_model(n_changepoints, samples, tune, chains)
        
        # Update global results after running models
        model_results = model_runner_instance.results

        comparison = model_runner_instance.compare_models()
        
        # Save results
        output_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'processed', 'model_results.pkl')
        model_runner_instance.save_results(output_path)
        
        return jsonify({
            'status': 'success',
            'message': 'Models fitted successfully',
            'comparison': comparison
        })
        
    except Exception as e:
        print(f"Error running model: {e}")
        return jsonify({'error': str(e)}), 500

@model_bp.route('/diagnostics', methods=['GET'])
def get_model_diagnostics():
    """Get model diagnostics and convergence checks."""
    if model_results is None or 'event_model' not in model_results or 'trace' not in model_results['event_model']:
        return jsonify({'error': 'Event model not fitted or results not loaded.'}), 500

    event_trace = model_results['event_model']['trace']
    event_model_pymc = model_runner_instance.event_model.model # Get the PyMC3 model object
    
    # Prepare data for diagnostics
    y, X_events = model_runner_instance.prepare_data()
    event_names = model_runner_instance.event_cols

    diagnostics_obj = ModelDiagnostics(event_trace, event_model_pymc, model_runner_instance.data)
    report = diagnostics_obj.generate_summary_report()

    # Convert ArviZ objects to serializable formats
    summary_df = report['summary']
    waic_obj = report['waic']

    diagnostics_output = {
        'convergence': {
            'r_hat_max': report['max_rhat'].item() if not pd.isna(report['max_rhat']) else 'N/A',
            'effective_sample_size_min': report['n_effective_samples'].item() if not pd.isna(report['n_effective_samples']) else 'N/A',
            'all_below_1.1': report['max_rhat'] < 1.05 if not pd.isna(report['max_rhat']) else False
        },
        'model_comparison': {
            'basic_model_waic': model_results['basic_model']['waic'].waic.item() if 'basic_model' in model_results else 'N/A',
            'event_model_waic': waic_obj.waic.item(),
            'waic_difference': (model_results['basic_model']['waic'].waic - waic_obj.waic).item() if 'basic_model' in model_results else 'N/A',
            'preferred_model': 'event_model' if waic_obj.waic < (model_results['basic_model']['waic'].waic if 'basic_model' in model_results else float('inf')) else 'basic_model'
        },
        'summary_statistics': summary_df.to_dict(orient='index')
    }
    
    return jsonify(diagnostics_output)