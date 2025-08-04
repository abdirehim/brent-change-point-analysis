"""
PyMC3 Model Runner for Brent Change Point Analysis

This module contains the core PyMC3 models for Bayesian change point detection
in Brent oil prices, including models with and without event covariates.
"""

import numpy as np
import pandas as pd
import pymc3 as pm
import arviz as az
from typing import Tuple, Dict, Optional, List
import warnings
warnings.filterwarnings('ignore')


class BrentChangePointModel:
    """
    Base class for Brent oil price change point models.
    """
    
    def __init__(self, data: pd.DataFrame, n_changepoints: int = 5):
        """
        Initialize the change point model.
        
        Parameters:
        -----------
        data : pd.DataFrame
            DataFrame containing price data and features
        n_changepoints : int
            Number of change points to detect
        """
        self.data = data
        self.n_changepoints = n_changepoints
        self.model = None
        self.trace = None
        
    def fit(self, samples: int = 2000, tune: int = 1000, chains: int = 2) -> az.InferenceData:
        """
        Fit the model using MCMC sampling.
        
        Parameters:
        -----------
        samples : int
            Number of posterior samples
        tune : int
            Number of tuning steps
        chains : int
            Number of MCMC chains
            
        Returns:
        --------
        az.InferenceData
            Posterior samples and diagnostics
        """
        if self.model is None:
            raise ValueError("Model not defined. Call build_model() first.")
            
        with self.model:
            self.trace = pm.sample(samples, tune=tune, chains=chains, 
                                 return_inferencedata=True)
        return self.trace
    
    def get_changepoints(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract change point posterior distributions.
        
        Returns:
        --------
        Tuple[np.ndarray, np.ndarray]
            Mean change points and HDI intervals
        """
        if self.trace is None:
            raise ValueError("Model not fitted. Call fit() first.")
            
        changepoints_posterior = self.trace.posterior['changepoints_sorted'].values
        changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
        changepoints_hdi = az.hdi(self.trace, var_names=['changepoints_sorted'])
        
        return changepoints_mean, changepoints_hdi['changepoints_sorted']


class BasicChangePointModel(BrentChangePointModel):
    """
    Basic change point model without covariates.
    """
    
    def build_model(self, y: np.ndarray) -> pm.Model:
        """
        Build the basic change point model.
        
        Parameters:
        -----------
        y : np.ndarray
            Target variable (returns)
            
        Returns:
        --------
        pm.Model
            PyMC3 model
        """
        n = len(y)
        
        with pm.Model() as model:
            # Prior for change point locations
            changepoint_probs = pm.Beta('changepoint_probs', alpha=1, beta=1, 
                                      shape=self.n_changepoints)
            changepoints = pm.Deterministic('changepoints', 
                                          (changepoint_probs * (n-1)).astype(int))
            
            # Sort change points to ensure chronological order
            changepoints_sorted = pm.Deterministic('changepoints_sorted', 
                                                 pm.math.sort(changepoints))
            
            # Prior for segment means
            segment_means = pm.Normal('segment_means', mu=0, sigma=0.1, 
                                    shape=self.n_changepoints+1)
            
            # Prior for segment standard deviations
            segment_sigmas = pm.HalfNormal('segment_sigmas', sigma=0.1, 
                                         shape=self.n_changepoints+1)
            
            # Assign observations to segments
            segment_idx = pm.Deterministic('segment_idx', 
                                         pm.math.searchsorted(changepoints_sorted, np.arange(n)))
            
            # Likelihood
            mu = segment_means[segment_idx]
            sigma = segment_sigmas[segment_idx]
            
            likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=y)
            
        self.model = model
        return model


class EventCovariateModel(BrentChangePointModel):
    """
    Change point model with event covariates.
    """
    
    def build_model(self, y: np.ndarray, X_events: np.ndarray) -> pm.Model:
        """
        Build the change point model with event covariates.
        
        Parameters:
        -----------
        y : np.ndarray
            Target variable (returns)
        X_events : np.ndarray
            Event feature matrix
            
        Returns:
        --------
        pm.Model
            PyMC3 model
        """
        n = len(y)
        n_features = X_events.shape[1]
        
        with pm.Model() as model:
            # Prior for change point locations
            changepoint_probs = pm.Beta('changepoint_probs', alpha=1, beta=1, 
                                      shape=self.n_changepoints)
            changepoints = pm.Deterministic('changepoints', 
                                          (changepoint_probs * (n-1)).astype(int))
            changepoints_sorted = pm.Deterministic('changepoints_sorted', 
                                                 pm.math.sort(changepoints))
            
            # Prior for segment intercepts
            segment_intercepts = pm.Normal('segment_intercepts', mu=0, sigma=0.1, 
                                         shape=self.n_changepoints+1)
            
            # Prior for event coefficients (shared across segments)
            event_coefficients = pm.Normal('event_coefficients', mu=0, sigma=0.05, 
                                         shape=n_features)
            
            # Prior for segment standard deviations
            segment_sigmas = pm.HalfNormal('segment_sigmas', sigma=0.1, 
                                         shape=self.n_changepoints+1)
            
            # Assign observations to segments
            segment_idx = pm.Deterministic('segment_idx', 
                                         pm.math.searchsorted(changepoints_sorted, np.arange(n)))
            
            # Linear predictor
            event_effect = pm.math.dot(X_events, event_coefficients)
            segment_effect = segment_intercepts[segment_idx]
            mu = segment_effect + event_effect
            
            # Likelihood
            sigma = segment_sigmas[segment_idx]
            likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=y)
            
        self.model = model
        return model


class ModelRunner:
    """
    High-level interface for running change point models.
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the model runner.
        
        Parameters:
        -----------
        data_path : str
            Path to the processed data file
        """
        self.data = pd.read_csv(data_path)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.basic_model = None
        self.event_model = None
        self.results = {}
        
    def prepare_data(self, target_col: str = 'Returns', 
                    event_cols: Optional[List[str]] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare data for modeling.
        
        Parameters:
        -----------
        target_col : str
            Name of the target variable column
        event_cols : List[str], optional
            List of event feature columns
            
        Returns:
        --------
        Tuple[np.ndarray, np.ndarray]
            Target variable and event features
        """
        # Default event columns if not specified
        if event_cols is None:
            event_cols = ['Event_Count_30d', 'High_Impact_Event_30d', 'War_Event_30d', 
                         'OPEC_Event_30d', 'Crisis_Event_30d', 'Days_Since_Last_Event']
        
        # Extract target variable
        y = self.data[target_col].values
        
        # Extract and standardize event features
        X_events = self.data[event_cols].values
        X_events = (X_events - X_events.mean(axis=0)) / X_events.std(axis=0)
        
        # Remove NaN values
        valid_idx = ~(np.isnan(y) | np.isnan(X_events).any(axis=1))
        y = y[valid_idx]
        X_events = X_events[valid_idx]
        
        return y, X_events
    
    def run_basic_model(self, n_changepoints: int = 5, 
                       samples: int = 2000, tune: int = 1000, 
                       chains: int = 2) -> az.InferenceData:
        """
        Run the basic change point model.
        
        Parameters:
        -----------
        n_changepoints : int
            Number of change points to detect
        samples : int
            Number of posterior samples
        tune : int
            Number of tuning steps
        chains : int
            Number of MCMC chains
            
        Returns:
        --------
        az.InferenceData
            Posterior samples
        """
        y, _ = self.prepare_data()
        
        self.basic_model = BasicChangePointModel(self.data, n_changepoints)
        self.basic_model.build_model(y)
        trace = self.basic_model.fit(samples, tune, chains)
        
        self.results['basic_model'] = {
            'trace': trace,
            'waic': az.waic(trace, self.basic_model.model)
        }
        
        return trace
    
    def run_event_model(self, n_changepoints: int = 5,
                       samples: int = 2000, tune: int = 1000,
                       chains: int = 2) -> az.InferenceData:
        """
        Run the change point model with event covariates.
        
        Parameters:
        -----------
        n_changepoints : int
            Number of change points to detect
        samples : int
            Number of posterior samples
        tune : int
            Number of tuning steps
        chains : int
            Number of MCMC chains
            
        Returns:
        --------
        az.InferenceData
            Posterior samples
        """
        y, X_events = self.prepare_data()
        
        self.event_model = EventCovariateModel(self.data, n_changepoints)
        self.event_model.build_model(y, X_events)
        trace = self.event_model.fit(samples, tune, chains)
        
        self.results['event_model'] = {
            'trace': trace,
            'waic': az.waic(trace, self.event_model.model)
        }
        
        return trace
    
    def compare_models(self) -> Dict:
        """
        Compare the basic and event models.
        
        Returns:
        --------
        Dict
            Model comparison results
        """
        if 'basic_model' not in self.results or 'event_model' not in self.results:
            raise ValueError("Both models must be fitted before comparison.")
        
        basic_waic = self.results['basic_model']['waic']
        event_waic = self.results['event_model']['waic']
        
        comparison = {
            'basic_waic': basic_waic.waic,
            'basic_waic_se': basic_waic.waic_se,
            'event_waic': event_waic.waic,
            'event_waic_se': event_waic.waic_se,
            'waic_difference': basic_waic.waic - event_waic.waic,
            'preferred_model': 'event_model' if event_waic.waic < basic_waic.waic else 'basic_model'
        }
        
        return comparison
    
    def save_results(self, output_path: str):
        """
        Save model results to file.
        
        Parameters:
        -----------
        output_path : str
            Path to save the results
        """
        import pickle
        
        with open(output_path, 'wb') as f:
            pickle.dump(self.results, f)
        
        print(f"Results saved to {output_path}")


def run_analysis(data_path: str, output_path: str, 
                n_changepoints: int = 5) -> ModelRunner:
    """
    Run complete change point analysis.
    
    Parameters:
    -----------
    data_path : str
        Path to the processed data file
    output_path : str
        Path to save results
    n_changepoints : int
        Number of change points to detect
        
    Returns:
    --------
    ModelRunner
        Fitted model runner with results
    """
    # Initialize runner
    runner = ModelRunner(data_path)
    
    # Run basic model
    print("Running basic change point model...")
    runner.run_basic_model(n_changepoints)
    
    # Run event model
    print("Running event-augmented change point model...")
    runner.run_event_model(n_changepoints)
    
    # Compare models
    comparison = runner.compare_models()
    print(f"Model comparison: {comparison}")
    
    # Save results
    runner.save_results(output_path)
    
    return runner


if __name__ == "__main__":
    # Example usage
    data_path = "../data/processed/events_aligned.csv"
    output_path = "../data/processed/model_results.pkl"
    
    runner = run_analysis(data_path, output_path, n_changepoints=5) 