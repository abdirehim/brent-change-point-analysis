"""
Event Data Routes

This module contains Flask routes for handling geopolitical and economic event data endpoints.
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random

event_bp = Blueprint('events', __name__, url_prefix='/api/events')

@event_bp.route('/summary', methods=['GET'])
def get_event_summary():
    """Get summary statistics for event data."""
    try:
        # Mock event summary data
        summary = {
            'total_events': 150,
            'geopolitical_count': 85,
            'economic_count': 65,
            'date_range': {
                'start': '2010-01-01',
                'end': '2024-01-01'
            },
            'categories': [
                {'name': 'Wars/Conflicts', 'count': 25},
                {'name': 'Sanctions', 'count': 30},
                {'name': 'OPEC Decisions', 'count': 20},
                {'name': 'Economic Crises', 'count': 15},
                {'name': 'Supply Disruptions', 'count': 35},
                {'name': 'Demand Shocks', 'count': 25}
            ],
            'recent_events': [
                {
                    'date': '2024-01-15',
                    'description': 'OPEC+ announces production cuts',
                    'category': 'OPEC Decisions',
                    'price_impact': 5.2
                },
                {
                    'date': '2024-01-10',
                    'description': 'Geopolitical tensions in Middle East',
                    'category': 'Wars/Conflicts',
                    'price_impact': 3.8
                },
                {
                    'date': '2024-01-05',
                    'description': 'Economic sanctions on major oil producer',
                    'category': 'Sanctions',
                    'price_impact': 4.1
                }
            ]
        }
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@event_bp.route('/list', methods=['GET'])
def get_events_list():
    """Get a list of all events with filtering options."""
    try:
        event_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        category = request.args.get('category')
        
        # Mock events data
        events = [
            {
                'id': 1,
                'date': '2024-01-15',
                'description': 'OPEC+ announces production cuts of 1 million bpd',
                'category': 'OPEC Decisions',
                'type': 'economic',
                'impact_score': 0.8,
                'price_impact': 5.2,
                'confidence': 0.85
            },
            {
                'id': 2,
                'date': '2024-01-10',
                'description': 'Geopolitical tensions escalate in Middle East',
                'category': 'Wars/Conflicts',
                'type': 'geopolitical',
                'impact_score': 0.9,
                'price_impact': 3.8,
                'confidence': 0.75
            },
            {
                'id': 3,
                'date': '2024-01-05',
                'description': 'Economic sanctions imposed on major oil producer',
                'category': 'Sanctions',
                'type': 'geopolitical',
                'impact_score': 0.7,
                'price_impact': 4.1,
                'confidence': 0.80
            }
        ]
        
        # Apply filters if provided
        if event_type:
            events = [e for e in events if e['type'] == event_type]
        if category:
            events = [e for e in events if e['category'] == category]
        
        return jsonify(events)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@event_bp.route('/categories', methods=['GET'])
def get_event_categories():
    """Get all available event categories."""
    try:
        categories = [
            {
                'name': 'Wars/Conflicts',
                'description': 'Military conflicts and wars affecting oil supply',
                'count': 25,
                'avg_impact': 4.2
            },
            {
                'name': 'Sanctions',
                'description': 'Economic sanctions on oil-producing countries',
                'count': 30,
                'avg_impact': 3.8
            },
            {
                'name': 'OPEC Decisions',
                'description': 'OPEC and OPEC+ production decisions',
                'count': 20,
                'avg_impact': 2.5
            },
            {
                'name': 'Economic Crises',
                'description': 'Major economic crises affecting oil demand',
                'count': 15,
                'avg_impact': 3.1
            },
            {
                'name': 'Supply Disruptions',
                'description': 'Infrastructure and supply chain disruptions',
                'count': 35,
                'avg_impact': 2.8
            },
            {
                'name': 'Demand Shocks',
                'description': 'Sudden changes in oil demand patterns',
                'count': 25,
                'avg_impact': 2.3
            }
        ]
        
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@event_bp.route('/impact-analysis', methods=['GET'])
def get_impact_analysis():
    """Get detailed impact analysis of events on oil prices."""
    try:
        # Mock impact analysis
        analysis = {
            'overall_impact': {
                'total_events': 150,
                'positive_impact': 45,
                'negative_impact': 105,
                'avg_impact_magnitude': 3.2
            },
            'impact_by_category': [
                {
                    'category': 'Wars/Conflicts',
                    'avg_impact': 4.2,
                    'frequency': 0.17,
                    'volatility_contribution': 0.25
                },
                {
                    'category': 'Sanctions',
                    'avg_impact': 3.8,
                    'frequency': 0.20,
                    'volatility_contribution': 0.22
                },
                {
                    'category': 'OPEC Decisions',
                    'avg_impact': 2.5,
                    'frequency': 0.13,
                    'volatility_contribution': 0.15
                }
            ],
            'temporal_analysis': {
                'impact_decay_rate': 0.15,
                'lag_effect_days': 3,
                'persistence_factor': 0.30
            }
        }
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 