"""
Event Data Routes

This module contains Flask routes for handling geopolitical and economic event data endpoints.
"""

from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

event_bp = Blueprint('events', __name__, url_prefix='/api/events')

# Load events_aligned.csv once when the blueprint is registered
file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'processed', 'events_aligned.csv')
events_data = pd.read_csv(file_path)
events_data['Date'] = pd.to_datetime(events_data['Date'])

# Define event columns based on the events.csv file
EVENT_COLUMNS = [
    'Gulf War',
    'Asian Financial Crisis',
    '9/11 Attacks',
    'Venezuelan General Strike',
    'Invasion of Iraq',
    'Global Financial Crisis (Peak Oil Price)',
    'Global Financial Crisis (Bottom Oil Price)',
    'Arab Spring',
    'COVID-19 Pandemic (Oil Price Crash)',
    'Russian Invasion of Ukraine',
    'Israel-Hamas Conflict'
]

@event_bp.route('/summary', methods=['GET'])
def get_event_summary():
    """Get summary statistics for event data."""
    try:
        # Filter out rows where no events occurred (all event columns are 0)
        active_events = events_data[events_data[EVENT_COLUMNS].sum(axis=1) > 0]

        total_events = active_events[EVENT_COLUMNS].sum().sum()
        
        # For geopolitical and economic counts, we need to categorize events
        # This is a simplified categorization based on event names
        geopolitical_events = ['Gulf War', '9/11 Attacks', 'Invasion of Iraq', 'Russian Invasion of Ukraine', 'Israel-Hamas Conflict']
        economic_events = ['Asian Financial Crisis', 'Venezuelan General Strike', 'Global Financial Crisis (Peak Oil Price)', 'Global Financial Crisis (Bottom Oil Price)', 'Arab Spring', 'COVID-19 Pandemic (Oil Price Crash)']

        geopolitical_count = active_events[geopolitical_events].sum().sum()
        economic_count = active_events[economic_events].sum().sum()

        summary = {
            'total_events': int(total_events),
            'geopolitical_count': int(geopolitical_count),
            'economic_count': int(economic_count),
            'date_range': {
                'start': events_data['Date'].min().strftime('%Y-%m-%d'),
                'end': events_data['Date'].max().strftime('%Y-%m-%d')
            },
            'categories': [
                {'name': 'Wars/Conflicts', 'count': int(active_events[['Gulf War', 'Invasion of Iraq', 'Russian Invasion of Ukraine', 'Israel-Hamas Conflict']].sum().sum())},
                {'name': 'Economic Crises', 'count': int(active_events[['Asian Financial Crisis', 'Global Financial Crisis (Peak Oil Price)', 'Global Financial Crisis (Bottom Oil Price)', 'COVID-19 Pandemic (Oil Price Crash)']].sum().sum())},
                # Add other categories as needed based on EVENT_COLUMNS
            ],
            'recent_events': [] # This would require more complex logic to extract actual recent events
        }
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@event_bp.route('/list', methods=['GET'])
def get_events_list():
    """Get a list of all events with filtering options."""
    try:
        event_type = request.args.get('type')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        category = request.args.get('category')
        
        filtered_events = events_data[events_data[EVENT_COLUMNS].sum(axis=1) > 0].copy()

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            filtered_events = filtered_events[filtered_events['Date'] >= start_date]
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            filtered_events = filtered_events[filtered_events['Date'] <= end_date]
        
        # Simplified category filtering - needs more robust mapping if categories are complex
        if category:
            if category == 'Wars/Conflicts':
                filtered_events = filtered_events[filtered_events[['Gulf War', 'Invasion of Iraq', 'Russian Invasion of Ukraine', 'Israel-Hamas Conflict']].sum(axis=1) > 0]
            elif category == 'Economic Crises':
                filtered_events = filtered_events[filtered_events[['Asian Financial Crisis', 'Global Financial Crisis (Peak Oil Price)', 'Global Financial Crisis (Bottom Oil Price)', 'COVID-19 Pandemic (Oil Price Crash)']].sum(axis=1) > 0]
            # Add more category filtering as needed

        events_list = []
        for index, row in filtered_events.iterrows():
            for event_col in EVENT_COLUMNS:
                if row[event_col] == 1:
                    events_list.append({
                        'id': index, # Using index as a simple ID
                        'date': row['Date'].strftime('%Y-%m-%d'),
                        'description': event_col, # Using column name as description for now
                        'category': 'Unknown', # Needs proper mapping
                        'type': 'Unknown', # Needs proper mapping
                        'impact_score': row['High_Impact_Event_30d'], # Example, needs actual impact score
                        'price_impact': row['log_return'], # Example, needs actual price impact
                        'confidence': 1.0 # Placeholder
                    })
        
        return jsonify(events_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@event_bp.route('/categories', methods=['GET'])
def get_event_categories():
    """Get all available event categories."""
    try:
        # Dynamically generate categories based on EVENT_COLUMNS or predefined groups
        categories = [
            {'name': 'Wars/Conflicts', 'description': 'Military conflicts and wars affecting oil supply'},
            {'name': 'Economic Crises', 'description': 'Major economic crises affecting oil demand'},
            # Add more categories as needed
        ]
        
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@event_bp.route('/impact-analysis', methods=['GET'])
def get_impact_analysis():
    """Get detailed impact analysis of events on oil prices."""
    try:
        # This would ideally come from model results, but for now, use aggregated data
        total_events = events_data[EVENT_COLUMNS].sum().sum()
        avg_log_return_around_events = events_data[events_data[EVENT_COLUMNS].sum(axis=1) > 0]['log_return'].mean()
        avg_volatility_around_events = events_data[events_data[EVENT_COLUMNS].sum(axis=1) > 0]['volatility'].mean()

        analysis = {
            'overall_impact': {
                'total_events': int(total_events),
                'avg_log_return_around_events': float(avg_log_return_around_events) if not pd.isna(avg_log_return_around_events) else 0.0,
                'avg_volatility_around_events': float(avg_volatility_around_events) if not pd.isna(avg_volatility_around_events) else 0.0,
            },
            'impact_by_category': [
                # This would be more complex, requiring mapping events to categories and then calculating impact
                # For now, providing placeholders or simplified calculations
                {'category': 'Wars/Conflicts', 'avg_impact': 0.0, 'frequency': 0.0, 'volatility_contribution': 0.0},
                {'category': 'Economic Crises', 'avg_impact': 0.0, 'frequency': 0.0, 'volatility_contribution': 0.0},
            ],
            'temporal_analysis': {
                'lag_effect_days': 'To be determined by model',
                'persistence_factor': 'To be determined by model'
            }
        }
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500