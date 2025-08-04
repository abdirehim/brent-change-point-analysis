# Raw Data Directory

This directory contains the original, unprocessed data files for the Brent change point analysis.

## Expected Files

### Brent Oil Price Data
- `brent_prices.csv` - Historical Brent crude oil prices (daily/weekly)
  - Columns: Date, Price, Volume (if available)
  - Sources: EIA, FRED, Yahoo Finance

### Event Data
- `geopolitical_events.csv` - Major geopolitical events affecting oil markets
  - Columns: Date, Event_Type, Description, Region, Impact_Level
  - Event types: Wars, Sanctions, OPEC decisions, Political crises

- `economic_events.csv` - Economic events and indicators
  - Columns: Date, Event_Type, Description, Impact_Level
  - Event types: Recessions, Financial crises, Policy changes

## Data Sources

1. **Brent Oil Prices**: 
   - EIA (Energy Information Administration)
   - FRED (Federal Reserve Economic Data)
   - Yahoo Finance API

2. **Geopolitical Events**:
   - News databases
   - Academic literature
   - Government reports

3. **Economic Indicators**:
   - FRED API
   - World Bank Data
   - IMF Data

## Data Format Standards

- All dates should be in YYYY-MM-DD format
- Missing values should be marked as NaN or NULL
- Currency values should be in USD
- Include data source and last update timestamp in file headers

## Notes

- Keep original data files unchanged
- Document any data quality issues
- Include data dictionaries for complex datasets 