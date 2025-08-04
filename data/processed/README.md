# Processed Data Directory

This directory contains cleaned, transformed, and feature-engineered datasets ready for modeling.

## Expected Files

### Cleaned Price Data
- `brent_prices_clean.csv` - Cleaned Brent price time series
  - Handled missing values
  - Removed outliers
  - Consistent date format

### Event-Aligned Data
- `events_aligned.csv` - Events aligned with price data
  - Matched event dates with price observations
  - Added event impact indicators
  - Created event windows

### Feature Engineering
- `price_features.csv` - Engineered price features
  - Returns (daily, weekly, monthly)
  - Volatility measures
  - Moving averages
  - Technical indicators

- `event_features.csv` - Event-based features
  - Event frequency by period
  - Cumulative event impact
  - Event type indicators

## Processing Steps

1. **Data Cleaning**
   - Handle missing values
   - Remove duplicates
   - Standardize formats

2. **Feature Engineering**
   - Calculate returns and volatility
   - Create event indicators
   - Generate time-based features

3. **Data Validation**
   - Check for data quality issues
   - Validate date ranges
   - Ensure consistency

## File Naming Convention

- `{dataset_name}_clean.csv` - Cleaned version
- `{dataset_name}_features.csv` - With engineered features
- `{dataset_name}_aligned.csv` - Aligned with other datasets

## Notes

- Document all processing steps
- Include data quality metrics
- Version control processed datasets 