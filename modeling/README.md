# Modeling Documentation

## Overview

This module implements Bayesian change point detection models for analyzing structural breaks in Brent oil prices using PyMC3.

## Model Classes

### BrentChangePointModel (Base Class)
Base class for all change point models with common functionality:
- Model fitting with MCMC sampling
- Change point extraction and analysis
- Posterior distribution handling

### BasicChangePointModel
Simple change point model without covariates:
- Detects structural breaks in mean and variance
- Uses Beta priors for change point locations
- Suitable for exploratory analysis

### EventCovariateModel
Advanced model incorporating event data:
- Includes geopolitical and economic events
- Shared event coefficients across segments
- Better predictive performance

## Usage Examples

### Basic Model
```python
from modeling import BasicChangePointModel
import numpy as np

# Prepare data
returns = np.random.normal(0, 0.1, 1000)

# Initialize and fit model
model = BasicChangePointModel(data, n_changepoints=3)
model.build_model(returns)
trace = model.fit(samples=1000, tune=500)

# Extract change points
changepoints, hdi = model.get_changepoints()
```

### Event Model
```python
from modeling import EventCovariateModel
import numpy as np

# Prepare data with events
returns = np.random.normal(0, 0.1, 1000)
events = np.random.binomial(1, 0.1, (1000, 6))

# Initialize and fit model
model = EventCovariateModel(data, n_changepoints=3)
model.build_model(returns, events)
trace = model.fit(samples=2000, tune=1000)
```

### High-Level Interface
```python
from modeling import run_analysis

# Run complete analysis
runner = run_analysis(
    data_path="data/processed/events_aligned.csv",
    output_path="results/model_results.pkl",
    n_changepoints=5
)
```

## Model Parameters

### Change Point Priors
- **changepoint_probs**: Beta(1,1) priors for change point locations
- **segment_means**: Normal(0, 0.1) priors for segment intercepts
- **segment_sigmas**: HalfNormal(0.1) priors for segment standard deviations

### Event Coefficients
- **event_coefficients**: Normal(0, 0.05) priors for event impacts
- Shared across all segments for stability

## Model Diagnostics

### Convergence Checks
- R-hat statistics (should be < 1.1)
- Effective sample size (should be > 400)
- Trace plots for visual inspection

### Model Comparison
- WAIC (Widely Applicable Information Criterion)
- Leave-one-out cross-validation
- Posterior predictive checks

## Performance Considerations

### Memory Usage
- Large datasets: Use fewer samples (1000-1500)
- Multiple models: Reduce chains to 2
- Limited memory: Process in batches

### Computation Time
- Development: 500 samples, 250 tune
- Production: 2000+ samples, 1000+ tune
- Parallel: Use 2-4 chains

### Optimization Tips
1. Start with basic model for exploration
2. Use event model for final analysis
3. Validate convergence before interpretation
4. Cache results for repeated analysis

## Troubleshooting

### Common Issues
1. **Divergences**: Increase tune steps or use different step size
2. **Poor mixing**: Check parameter initialization
3. **Memory errors**: Reduce sample size or data size
4. **Slow convergence**: Increase tune steps or samples

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## References

See `references/bayesian_change_point_refs.md` for academic references and theoretical background.