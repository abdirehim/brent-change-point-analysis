"""
Data Loader Utility

This module provides utilities for loading and processing data in the Flask backend.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Utility class for loading and processing data files."""
    
    def __init__(self, data_dir: str = "../data"):
        """
        Initialize the DataLoader.
        
        Args:
            data_dir: Path to the data directory
        """
        self.data_dir = data_dir
        self.processed_dir = os.path.join(data_dir, "processed")
        self.raw_dir = os.path.join(data_dir, "raw")
        
        # Ensure directories exist
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs(self.raw_dir, exist_ok=True)
    
    def load_price_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        Load Brent oil price data.
        
        Args:
            file_path: Optional path to price data file
            
        Returns:
            DataFrame with price data
        """
        if file_path is None:
            file_path = os.path.join(self.processed_dir, "brent_prices_clean.csv")
        
        try:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                logger.info(f"Loaded price data from {file_path}")
                return df
            else:
                logger.warning(f"Price data file not found: {file_path}")
                return self._generate_mock_price_data()
        except Exception as e:
            logger.error(f"Error loading price data: {e}")
            return self._generate_mock_price_data()
    
    def load_event_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        Load event data.
        
        Args:
            file_path: Optional path to event data file
            
        Returns:
            DataFrame with event data
        """
        if file_path is None:
            file_path = os.path.join(self.processed_dir, "events_aligned.csv")
        
        try:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df['date'] = pd.to_datetime(df['date'])
                logger.info(f"Loaded event data from {file_path}")
                return df
            else:
                logger.warning(f"Event data file not found: {file_path}")
                return self._generate_mock_event_data()
        except Exception as e:
            logger.error(f"Error loading event data: {e}")
            return self._generate_mock_event_data()
    
    def load_model_results(self, file_path: Optional[str] = None) -> Dict:
        """
        Load pre-computed model results.
        
        Args:
            file_path: Optional path to model results file
            
        Returns:
            Dictionary with model results
        """
        if file_path is None:
            file_path = os.path.join(self.processed_dir, "model_results.json")
        
        try:
            if os.path.exists(file_path):
                import json
                with open(file_path, 'r') as f:
                    results = json.load(f)
                logger.info(f"Loaded model results from {file_path}")
                return results
            else:
                logger.warning(f"Model results file not found: {file_path}")
                return self._generate_mock_model_results()
        except Exception as e:
            logger.error(f"Error loading model results: {e}")
            return self._generate_mock_model_results()
    
    def get_data_summary(self) -> Dict:
        """
        Get summary statistics for all loaded data.
        
        Returns:
            Dictionary with data summary
        """
        try:
            price_data = self.load_price_data()
            event_data = self.load_event_data()
            
            summary = {
                'data_points': len(price_data),
                'date_range': {
                    'start': price_data.index.min().strftime('%Y-%m-%d'),
                    'end': price_data.index.max().strftime('%Y-%m-%d')
                },
                'price_range': {
                    'min': float(price_data['price'].min()),
                    'max': float(price_data['price'].max())
                },
                'price_stats': {
                    'mean': float(price_data['price'].mean()),
                    'std': float(price_data['price'].std()),
                    'median': float(price_data['price'].median())
                },
                'events_count': len(event_data) if not event_data.empty else 0,
                'missing_values': int(price_data['price'].isnull().sum()),
                'completeness': float((1 - price_data['price'].isnull().sum() / len(price_data)) * 100),
                'last_updated': datetime.now().isoformat()
            }
            
            return summary
        except Exception as e:
            logger.error(f"Error generating data summary: {e}")
            return self._generate_mock_summary()
    
    def _generate_mock_price_data(self) -> pd.DataFrame:
        """Generate mock price data for testing."""
        start_date = datetime(2020, 1, 1)
        dates = pd.date_range(start=start_date, periods=100, freq='D')
        
        # Generate realistic price data with trends and volatility
        np.random.seed(42)
        base_price = 70.0
        prices = []
        
        for i in range(100):
            # Add trend and volatility
            trend = 0.1 * np.sin(i / 10)  # Cyclical trend
            noise = np.random.normal(0, 2)  # Random noise
            price = base_price + trend + noise
            prices.append(max(20, price))  # Ensure positive prices
        
        df = pd.DataFrame({
            'price': prices
        }, index=dates)
        
        return df
    
    def _generate_mock_event_data(self) -> pd.DataFrame:
        """Generate mock event data for testing."""
        events = [
            {
                'date': '2024-01-15',
                'description': 'OPEC+ announces production cuts',
                'category': 'OPEC Decisions',
                'type': 'economic',
                'impact_score': 0.8
            },
            {
                'date': '2024-01-10',
                'description': 'Geopolitical tensions in Middle East',
                'category': 'Wars/Conflicts',
                'type': 'geopolitical',
                'impact_score': 0.9
            },
            {
                'date': '2024-01-05',
                'description': 'Economic sanctions on major oil producer',
                'category': 'Sanctions',
                'type': 'geopolitical',
                'impact_score': 0.7
            }
        ]
        
        df = pd.DataFrame(events)
        df['date'] = pd.to_datetime(df['date'])
        
        return df
    
    def _generate_mock_model_results(self) -> Dict:
        """Generate mock model results for testing."""
        return {
            'change_points': [
                {
                    'date': '2020-03-15',
                    'probability': 0.95,
                    'hdi_lower': '2020-03-10',
                    'hdi_upper': '2020-03-20'
                }
            ],
            'event_coefficients': [
                {
                    'event_type': 'Wars/Conflicts',
                    'coefficient': 0.045,
                    'significant': True
                }
            ],
            'model_status': {
                'status': 'ready',
                'waic_score': -1250.45
            }
        }
    
    def _generate_mock_summary(self) -> Dict:
        """Generate mock data summary for testing."""
        return {
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
            'events_count': 150,
            'missing_values': 0,
            'completeness': 100.0,
            'last_updated': datetime.now().isoformat()
        }

# Global data loader instance
data_loader = DataLoader() 