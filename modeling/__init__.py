"""
Bayesian Change Point Analysis Models

This package contains PyMC3 models and utilities for analyzing structural breaks
in Brent oil prices using Bayesian inference.
"""

from .model_runner import BrentChangePointModel, BasicChangePointModel, EventCovariateModel, ModelRunner, run_analysis
from .diagnostics import ModelDiagnostics, ChangePointVisualizer, run_diagnostics

__version__ = "1.0.0"
__author__ = "Data Science Team" 