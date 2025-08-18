# Configuration Guide

## Environment Variables

### Required
- `FLASK_ENV`: Set to `development` or `production`
- `FLASK_DEBUG`: Set to `True` for development, `False` for production

### Optional
- `DATA_PATH`: Custom path to data directory (default: `./data`)
- `MODEL_CACHE_PATH`: Path for model result caching (default: `./data/processed`)

## Model Configuration

### Change Point Detection Parameters
- `n_changepoints`: Number of change points to detect (default: 5, range: 1-10)
- `samples`: MCMC samples (default: 2000, min: 1000)
- `tune`: Tuning steps (default: 1000, min: 500)
- `chains`: MCMC chains (default: 2, range: 2-4)

### Event Features
Default event features used in analysis:
- `Event_Count_30d`: Count of events in 30-day window
- `High_Impact_Event_30d`: High-impact events indicator
- `War_Event_30d`: War-related events indicator
- `OPEC_Event_30d`: OPEC decision events indicator
- `Crisis_Event_30d`: Financial crisis events indicator
- `Days_Since_Last_Event`: Days since last major event

## Data Requirements

### Input Data Format
CSV files with the following columns:
- `Date`: Date in YYYY-MM-DD format
- `Price`: Oil price (numeric)
- Additional columns for events and features

### Data Validation
- Dates must be in chronological order
- Price values must be positive
- Missing values are forward-filled
- Minimum 100 observations required

## Performance Tuning

### Memory Usage
- Large datasets (>50k observations): Reduce MCMC samples to 1000
- Multiple models: Use single chain for faster execution
- Limited memory: Process data in chunks

### Computation Time
- Development: Use 500 samples, 250 tune steps
- Production: Use 2000+ samples, 1000+ tune steps
- Parallel processing: Increase chains (max 4)

## Troubleshooting

### Common Issues
1. **Memory errors**: Reduce sample size or data size
2. **Convergence warnings**: Increase tune steps or samples
3. **Slow performance**: Reduce chains or use smaller datasets
4. **Data loading errors**: Check file paths and formats

### Debug Mode
Enable debug logging by setting `FLASK_DEBUG=True` and adding:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```