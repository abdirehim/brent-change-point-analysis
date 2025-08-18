# Brent Change Point Analysis

## Project Overview

This project implements a comprehensive analysis of structural breaks in Brent oil prices using Bayesian modeling techniques. The analysis incorporates event-based correlations (wars, sanctions, geopolitical events) to identify and quantify change points in oil price dynamics.

## Objectives

- **Bayesian Change Point Detection**: Use PyMC3 to model structural breaks in Brent oil price time series
- **Event Correlation Analysis**: Align historical events with detected change points
- **Interactive Dashboard**: Provide a web-based interface for exploring analysis results
- **Comprehensive Reporting**: Generate detailed reports and presentations

## Tech Stack

### Backend & Modeling
- **Python 3.9+**: Core programming language
- **PyMC3**: Bayesian modeling and inference
- **ArviZ**: Bayesian diagnostics and visualization
- **Pandas/NumPy**: Data manipulation and analysis
- **Flask**: API backend for serving results

### Frontend
- **React**: Modern web interface
- **D3.js/Chart.js**: Interactive visualizations
- **Material-UI**: Component library

### Data & Reporting
- **Jupyter Notebooks**: Exploratory analysis and modeling
- **Plotly**: Interactive plots
- **LaTeX**: Report generation

## Project Structure

```
brent-change-point-analysis/
├── data/                    # Data storage
│   ├── raw/                # Raw Brent price & event data
│   ├── processed/          # Cleaned & transformed versions
│   └── external/           # Other data (e.g. GDP, FX)
├── notebooks/              # Jupyter notebooks for analysis
├── modeling/               # PyMC3 model implementation
├── dashboard/              # Web application
│   ├── backend/           # Flask API
│   └── frontend/          # React dashboard
├── reports/               # Generated reports and presentations
└── references/            # Literature and documentation
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Conda (recommended for PyMC3)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd brent-change-point-analysis
   ```

2. **Set up Python environment**
   ```bash
   conda env create -f environment.yml
   conda activate brent-analysis
   ```

3. **Install frontend dependencies**
   ```bash
   cd dashboard/frontend
   npm install
   ```

### Running the Analysis

1. **Start with notebooks**
   ```bash
   jupyter lab notebooks/
   ```
   - Run `01_eda_brent_prices.ipynb` for initial data exploration
   - Run `02_event_alignment.ipynb` for event correlation analysis
   - Run `03_bayesian_modeling.ipynb` for PyMC3 modeling

2. **Launch the dashboard**
   ```bash
   # Terminal 1: Start Flask backend
   cd dashboard/backend
   python app.py
   
   # Terminal 2: Start React frontend
   cd dashboard/frontend
   npm start
   ```

### Data Requirements

- Brent oil price time series (daily/weekly)
- Historical event data (wars, sanctions, OPEC decisions)
- Economic indicators (GDP, exchange rates)

## Documentation

- [API Documentation](API.md) - Complete API reference
- [Configuration Guide](CONFIGURATION.md) - Setup and configuration options
- [Data Documentation](data/README.md) - Data format and requirements
- [Model Documentation](modeling/README.md) - Model specifications and usage

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed via `conda env create -f environment.yml`
2. **Data loading errors**: Check file paths and data format requirements
3. **Model convergence**: Increase MCMC samples or tuning steps
4. **Memory issues**: Reduce data size or model complexity

### Performance Optimization

- Use fewer MCMC samples for development (500-1000)
- Enable parallel processing with multiple chains
- Cache model results to avoid re-computation

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Update documentation
5. Submit a pull request

## Security

This project includes security improvements:
- Input validation and sanitization
- Error handling for all API endpoints
- Safe data serialization practices

## License

MIT License - See LICENSE file for details

## Contact

For questions or support, please open an issue on the repository. 