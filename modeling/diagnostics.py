"""
Model Diagnostics and Visualization for Brent Change Point Analysis

This module provides comprehensive diagnostics and visualization tools
for the Bayesian change point models.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import arviz as az
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class ModelDiagnostics:
    """
    Comprehensive diagnostics for change point models.
    """
    
    def __init__(self, trace: az.InferenceData, model, data: pd.DataFrame):
        """
        Initialize diagnostics.
        
        Parameters:
        -----------
        trace : az.InferenceData
            Posterior samples
        model : pm.Model
            PyMC3 model
        data : pd.DataFrame
            Original data
        """
        self.trace = trace
        self.model = model
        self.data = data
        
    def plot_trace(self, var_names: Optional[List[str]] = None):
        """
        Plot trace plots for model parameters.
        
        Parameters:
        -----------
        var_names : List[str], optional
            Specific variables to plot
        """
        if var_names is None:
            var_names = ['segment_intercepts', 'event_coefficients', 'segment_sigmas']
        
        az.plot_trace(self.trace, var_names=var_names)
        plt.tight_layout()
        plt.show()
    
    def plot_posterior_predictive(self, y: np.ndarray):
        """
        Plot posterior predictive checks.
        
        Parameters:
        -----------
        y : np.ndarray
            Observed data
        """
        with self.model:
            ppc = pm.sample_posterior_predictive(self.trace, samples=1000)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # Histogram comparison
        axes[0, 0].hist(y, bins=30, alpha=0.7, label='Observed', density=True)
        axes[0, 0].hist(ppc['likelihood'].flatten(), bins=30, alpha=0.7, 
                       label='Predicted', density=True)
        axes[0, 0].set_title('Posterior Predictive Check: Histogram')
        axes[0, 0].legend()
        
        # Q-Q plot
        from scipy.stats import probplot
        probplot(y, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title('Q-Q Plot: Observed vs Normal')
        
        # Residuals
        residuals = y - ppc['likelihood'].mean(axis=0)
        axes[1, 0].scatter(range(len(residuals)), residuals, alpha=0.5)
        axes[1, 0].axhline(y=0, color='red', linestyle='--')
        axes[1, 0].set_title('Residuals')
        axes[1, 0].set_ylabel('Residual')
        
        # Residuals histogram
        axes[1, 1].hist(residuals, bins=30, alpha=0.7, edgecolor='black')
        axes[1, 1].set_title('Residuals Distribution')
        axes[1, 1].set_xlabel('Residual')
        
        plt.tight_layout()
        plt.show()
    
    def plot_changepoint_posteriors(self):
        """
        Plot posterior distributions of change points.
        """
        changepoints_posterior = self.trace.posterior['changepoints_sorted'].values
        changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
        changepoints_hdi = az.hdi(self.trace, var_names=['changepoints_sorted'])
        
        n_changepoints = changepoints_posterior.shape[-1]
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        for i in range(n_changepoints):
            cp_samples = changepoints_posterior[:, :, i].flatten()
            axes[i].hist(cp_samples, bins=30, alpha=0.7, edgecolor='black')
            axes[i].axvline(changepoints_mean[i], color='red', linestyle='--', label='Mean')
            axes[i].axvline(changepoints_hdi['changepoints_sorted'][i, 0], color='orange', 
                           linestyle='--', label='HDI Lower')
            axes[i].axvline(changepoints_hdi['changepoints_sorted'][i, 1], color='orange', 
                           linestyle='--', label='HDI Upper')
            axes[i].set_title(f'Change Point {i+1} Posterior')
            axes[i].set_xlabel('Time Index')
            axes[i].legend()
        
        plt.tight_layout()
        plt.show()
    
    def plot_event_coefficients(self, event_names: List[str]):
        """
        Plot posterior distributions of event coefficients.
        
        Parameters:
        -----------
        event_names : List[str]
            Names of event features
        """
        event_coeff_posterior = self.trace.posterior['event_coefficients'].values
        event_coeff_mean = event_coeff_posterior.mean(axis=(0, 1))
        event_coeff_hdi = az.hdi(self.trace, var_names=['event_coefficients'])
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        for i, feature in enumerate(event_names):
            coeff_samples = event_coeff_posterior[:, :, i].flatten()
            axes[i].hist(coeff_samples, bins=30, alpha=0.7, edgecolor='black')
            axes[i].axvline(event_coeff_mean[i], color='red', linestyle='--', label='Mean')
            axes[i].axvline(0, color='black', linestyle='-', alpha=0.5, label='Zero')
            axes[i].axvline(event_coeff_hdi['event_coefficients'][i, 0], color='orange', 
                           linestyle='--', label='HDI Lower')
            axes[i].axvline(event_coeff_hdi['event_coefficients'][i, 1], color='orange', 
                           linestyle='--', label='HDI Upper')
            axes[i].set_title(f'{feature} Coefficient')
            axes[i].set_xlabel('Coefficient Value')
            axes[i].legend()
        
        plt.tight_layout()
        plt.show()
    
    def generate_summary_report(self) -> Dict:
        """
        Generate comprehensive model summary.
        
        Returns:
        --------
        Dict
            Summary statistics and diagnostics
        """
        # Basic summary
        summary = az.summary(self.trace)
        
        # WAIC
        waic = az.waic(self.trace, self.model)
        
        # Effective sample size
        ess = az.ess(self.trace)
        
        # R-hat statistics
        rhat = az.rhat(self.trace)
        
        # Change point analysis
        changepoints_posterior = self.trace.posterior['changepoints_sorted'].values
        changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
        changepoints_hdi = az.hdi(self.trace, var_names=['changepoints_sorted'])
        
        report = {
            'summary': summary,
            'waic': waic,
            'ess': ess,
            'rhat': rhat,
            'changepoints_mean': changepoints_mean,
            'changepoints_hdi': changepoints_hdi,
            'n_effective_samples': ess.min(),
            'max_rhat': rhat.max()
        }
        
        return report


class ChangePointVisualizer:
    """
    Visualization tools for change point analysis results.
    """
    
    def __init__(self, data: pd.DataFrame, trace: az.InferenceData):
        """
        Initialize visualizer.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Original data
        trace : az.InferenceData
            Posterior samples
        """
        self.data = data
        self.trace = trace
        
    def plot_changepoints_on_series(self, y: np.ndarray, title: str = "Change Points"):
        """
        Plot change points overlaid on time series.
        
        Parameters:
        -----------
        y : np.ndarray
            Time series data
        title : str
            Plot title
        """
        changepoints_posterior = self.trace.posterior['changepoints_sorted'].values
        changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
        
        fig, ax = plt.subplots(figsize=(15, 6))
        
        # Plot time series
        ax.plot(self.data['Date'], y, alpha=0.7, label='Returns')
        
        # Add change points
        for i, mean_cp in enumerate(changepoints_mean):
            cp_date = self.data.iloc[int(mean_cp)]['Date']
            ax.axvline(x=cp_date, color='red', linestyle='--', alpha=0.8, 
                      label=f'CP {i+1}' if i == 0 else '')
            ax.text(cp_date, ax.get_ylim()[1], f'CP{i+1}', rotation=90, 
                   verticalalignment='top', fontsize=10)
        
        ax.set_title(title)
        ax.set_ylabel('Returns')
        ax.legend()
        plt.tight_layout()
        plt.show()
    
    def plot_segment_characteristics(self):
        """
        Plot characteristics of different segments.
        """
        changepoints_posterior = self.trace.posterior['changepoints_sorted'].values
        changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
        
        segment_intercepts_posterior = self.trace.posterior['segment_intercepts'].values
        segment_sigmas_posterior = self.trace.posterior['segment_sigmas'].values
        
        segment_intercepts_mean = segment_intercepts_posterior.mean(axis=(0, 1))
        segment_sigmas_mean = segment_sigmas_posterior.mean(axis=(0, 1))
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Segment intercepts
        axes[0, 0].bar(range(len(segment_intercepts_mean)), segment_intercepts_mean, alpha=0.7)
        axes[0, 0].set_title('Segment Intercepts')
        axes[0, 0].set_xlabel('Segment')
        axes[0, 0].set_ylabel('Intercept')
        
        # Segment sigmas
        axes[0, 1].bar(range(len(segment_sigmas_mean)), segment_sigmas_mean, alpha=0.7)
        axes[0, 1].set_title('Segment Standard Deviations')
        axes[0, 1].set_xlabel('Segment')
        axes[0, 1].set_ylabel('Sigma')
        
        # Segment durations
        segment_durations = []
        y = self.data['Returns'].values
        for i in range(len(changepoints_mean) + 1):
            start_idx = int(changepoints_mean[i-1]) if i > 0 else 0
            end_idx = int(changepoints_mean[i]) if i < len(changepoints_mean) else len(y)
            segment_durations.append(end_idx - start_idx)
        
        axes[1, 0].bar(range(len(segment_durations)), segment_durations, alpha=0.7)
        axes[1, 0].set_title('Segment Durations')
        axes[1, 0].set_xlabel('Segment')
        axes[1, 0].set_ylabel('Duration (days)')
        
        # Segment mean returns
        segment_means = []
        for i in range(len(changepoints_mean) + 1):
            start_idx = int(changepoints_mean[i-1]) if i > 0 else 0
            end_idx = int(changepoints_mean[i]) if i < len(changepoints_mean) else len(y)
            segment_means.append(y[start_idx:end_idx].mean())
        
        axes[1, 1].bar(range(len(segment_means)), segment_means, alpha=0.7)
        axes[1, 1].set_title('Segment Mean Returns')
        axes[1, 1].set_xlabel('Segment')
        axes[1, 1].set_ylabel('Mean Return')
        
        plt.tight_layout()
        plt.show()
    
    def create_interactive_dashboard(self, y: np.ndarray):
        """
        Create interactive dashboard with Plotly.
        
        Parameters:
        -----------
        y : np.ndarray
            Time series data
        """
        changepoints_posterior = self.trace.posterior['changepoints_sorted'].values
        changepoints_mean = changepoints_posterior.mean(axis=(0, 1))
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Time Series with Change Points', 'Segment Characteristics', 'Event Coefficients'),
            vertical_spacing=0.1
        )
        
        # Time series with change points
        fig.add_trace(
            go.Scatter(x=self.data['Date'], y=y, mode='lines', name='Returns'),
            row=1, col=1
        )
        
        for i, mean_cp in enumerate(changepoints_mean):
            cp_date = self.data.iloc[int(mean_cp)]['Date']
            fig.add_trace(
                go.Scatter(x=[cp_date], y=[y[int(mean_cp)]], mode='markers+text',
                          marker=dict(size=12, color='red', symbol='diamond'),
                          text=f'CP{i+1}', textposition='top center',
                          showlegend=False),
                row=1, col=1
            )
        
        # Segment characteristics
        segment_intercepts_posterior = self.trace.posterior['segment_intercepts'].values
        segment_intercepts_mean = segment_intercepts_posterior.mean(axis=(0, 1))
        
        fig.add_trace(
            go.Bar(x=list(range(len(segment_intercepts_mean))), 
                  y=segment_intercepts_mean, name='Segment Intercepts'),
            row=2, col=1
        )
        
        # Event coefficients
        event_coeff_posterior = self.trace.posterior['event_coefficients'].values
        event_coeff_mean = event_coeff_posterior.mean(axis=(0, 1))
        event_names = ['Event_Count_30d', 'High_Impact_Event_30d', 'War_Event_30d', 
                      'OPEC_Event_30d', 'Crisis_Event_30d', 'Days_Since_Last_Event']
        
        fig.add_trace(
            go.Bar(x=event_names, y=event_coeff_mean, name='Event Coefficients'),
            row=3, col=1
        )
        
        fig.update_layout(height=900, title_text="Change Point Analysis Dashboard")
        fig.show()


def run_diagnostics(trace: az.InferenceData, model, data: pd.DataFrame, 
                   y: np.ndarray, event_names: List[str]) -> ModelDiagnostics:
    """
    Run comprehensive model diagnostics.
    
    Parameters:
    -----------
    trace : az.InferenceData
        Posterior samples
    model : pm.Model
        PyMC3 model
    data : pd.DataFrame
        Original data
    y : np.ndarray
        Target variable
    event_names : List[str]
        Names of event features
        
    Returns:
    --------
    ModelDiagnostics
        Diagnostics object with results
    """
    diagnostics = ModelDiagnostics(trace, model, data)
    
    print("Running model diagnostics...")
    
    # Plot diagnostics
    diagnostics.plot_trace()
    diagnostics.plot_posterior_predictive(y)
    diagnostics.plot_changepoints_posteriors()
    diagnostics.plot_event_coefficients(event_names)
    
    # Generate summary report
    report = diagnostics.generate_summary_report()
    
    print(f"Model Summary:")
    print(f"WAIC: {report['waic'].waic:.2f}")
    print(f"Effective Sample Size: {report['n_effective_samples']:.0f}")
    print(f"Max R-hat: {report['max_rhat']:.3f}")
    
    return diagnostics


if __name__ == "__main__":
    # Example usage
    print("Diagnostics module loaded successfully.")
    print("Use run_diagnostics() function to analyze model results.") 