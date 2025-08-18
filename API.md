# API Documentation

## Overview
The Brent Change Point Analysis API provides endpoints for accessing oil price data, model results, and analysis outputs.

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### Health Check
**GET** `/health`

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "data_loaded": true,
  "model_loaded": true
}
```

### Data Summary
**GET** `/data/summary`

Returns summary statistics of the loaded data.

**Response:**
```json
{
  "total_observations": 10000,
  "date_range": {
    "start": "1987-05-20",
    "end": "2024-01-01"
  },
  "columns": ["Date", "Price", "Returns", "Volatility"],
  "price_stats": {
    "mean": 65.5,
    "std": 35.2,
    "min": 9.1,
    "max": 147.5
  }
}
```

### Price Series
**GET** `/data/price-series`

Returns time series price data with optional date filtering.

**Query Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format

**Response:**
```json
{
  "dates": ["2020-01-01", "2020-01-02"],
  "prices": [68.5, 69.2],
  "returns": [0.01, 0.02],
  "volatility": [0.25, 0.26]
}
```

### Change Points
**GET** `/model/changepoints`

Returns detected change points from the fitted model.

**Response:**
```json
{
  "changepoints": [
    {
      "id": 1,
      "date": "2008-09-15",
      "time_index": 5432,
      "hdi_lower": 5400,
      "hdi_upper": 5464
    }
  ]
}
```

### Event Coefficients
**GET** `/model/event-coefficients`

Returns event coefficient estimates from the model.

**Response:**
```json
{
  "coefficients": [
    {
      "feature": "War_Event_30d",
      "mean": 0.05,
      "hdi_lower": 0.02,
      "hdi_upper": 0.08,
      "significant": true
    }
  ]
}
```

### Run Model
**POST** `/model/run`

Fits the change point models with specified parameters.

**Request Body:**
```json
{
  "n_changepoints": 5,
  "samples": 2000,
  "tune": 1000,
  "chains": 2
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Models fitted successfully",
  "comparison": {
    "basic_waic": 1234.5,
    "event_waic": 1200.3,
    "preferred_model": "event_model"
  }
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error description"
}
```

Common HTTP status codes:
- `400`: Bad Request - Invalid parameters
- `500`: Internal Server Error - Server-side error
- `404`: Not Found - Endpoint not found

## Authentication

Currently, the API does not require authentication. In production, implement proper authentication and authorization.