import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import { PlayArrow, Refresh } from '@mui/icons-material';
import { apiService } from '../services/apiService';
import Plot from 'react-plotly.js';

const ModelAnalysis = () => {
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState(null);
  const [modelStatus, setModelStatus] = useState(null);
  const [changePoints, setChangePoints] = useState(null);
  const [segments, setSegments] = useState(null);
  const [priceSeries, setPriceSeries] = useState(null); // To fetch price series for plotting
  const [eventCoefficients, setEventCoefficients] = useState(null); // To fetch event coefficients

  useEffect(() => {
    fetchModelData();
  }, []);

  const fetchModelData = async () => {
    try {
      setLoading(true);
      const [status, changepoints, segmentData, priceData, coefficientsData] = await Promise.all([
        apiService.getModelStatus(),
        apiService.getChangePoints(),
        apiService.getSegments(),
        apiService.getPriceSeries(), // Fetch price series
        apiService.getEventCoefficients(), // Fetch event coefficients
      ]);
      setModelStatus(status);
      setChangePoints(changepoints.changepoints);
      setSegments(segmentData.segments);
      setPriceSeries(priceData); // Set price series data
      setEventCoefficients(coefficientsData.coefficients); // Set event coefficients
    } catch (err) {
      setError('Failed to load model data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const runModel = async () => {
    try {
      setRunning(true);
      setError(null);
      await apiService.runModel();
      await fetchModelData();
    } catch (err) {
      setError('Failed to run model');
      console.error(err);
    } finally {
      setRunning(false);
    }
  };

  // Plotly data for Price Series with Change Points
  const getPriceSeriesPlotData = () => {
    if (!priceSeries || !changePoints) return [];

    const priceTrace = {
      x: priceSeries.map(d => d.date),
      y: priceSeries.map(d => d.price),
      mode: 'lines',
      name: 'Brent Oil Price',
      line: { color: '#1976d2' },
    };

    const cpTraces = changePoints.map((cp, index) => ({
      x: [cp.date, cp.date],
      y: [Math.min(...priceSeries.map(d => d.price)), Math.max(...priceSeries.map(d => d.price))],
      mode: 'lines',
      name: `Change Point ${index + 1}`,
      line: { color: 'red', dash: 'dashdot', width: 1 },
      hoverinfo: 'text',
      text: `Change Point ${index + 1}<br>Date: ${cp.date}<br>HDI: ${cp.hdi_lower_date} - ${cp.hdi_upper_date}`,
    }));

    return [priceTrace, ...cpTraces];
  };

  const getPriceSeriesPlotLayout = () => ({
    title: 'Brent Oil Price with Detected Change Points',
    xaxis: { title: 'Date' },
    yaxis: { title: 'Price (USD)' },
    hovermode: 'closest',
    height: 400,
    margin: { t: 50, b: 50, l: 50, r: 50 },
  });

  // Plotly data for Segment Characteristics
  const getSegmentCharacteristicsPlotData = () => {
    if (!segments) return [];

    const segmentLabels = segments.map((s, index) => `Segment ${s.id}`);
    const meanReturns = segments.map(s => s.mean_log_return);
    const volatilities = segments.map(s => s.volatility);

    const meanReturnTrace = {
      x: segmentLabels,
      y: meanReturns,
      type: 'bar',
      name: 'Mean Log Return',
      marker: { color: '#4CAF50' },
    };

    const volatilityTrace = {
      x: segmentLabels,
      y: volatilities,
      type: 'bar',
      name: 'Volatility',
      marker: { color: '#FFC107' },
      yaxis: 'y2', // Use a secondary y-axis for volatility
    };

    return [meanReturnTrace, volatilityTrace];
  };

  const getSegmentCharacteristicsPlotLayout = () => ({
    title: 'Segment Mean Log Returns and Volatility',
    xaxis: { title: 'Segment' },
    yaxis: { title: 'Mean Log Return' },
    yaxis2: { // Secondary y-axis for volatility
      title: 'Volatility',
      overlaying: 'y',
      side: 'right',
    },
    barmode: 'group',
    height: 400,
    margin: { t: 50, b: 50, l: 50, r: 50 },
  });

  // Plotly data for Event Coefficients
  const getEventCoefficientsPlotData = () => {
    if (!eventCoefficients) return [];

    const features = eventCoefficients.map(c => c.feature);
    const means = eventCoefficients.map(c => c.mean);
    const hdiLowers = eventCoefficients.map(c => c.hdi_lower);
    const hdiUppers = eventCoefficients.map(c => c.hdi_upper);

    const errorBars = {
      type: 'data',
      array: hdiUppers.map((upper, i) => upper - means[i]),
      arrayminus: means.map((mean, i) => mean - hdiLowers[i]),
    };

    return [
      {
        x: features,
        y: means,
        type: 'bar',
        name: 'Event Coefficients',
        marker: { color: '#9C27B0' },
        error_y: errorBars,
      },
    ];
  };

  const getEventCoefficientsPlotLayout = () => ({
    title: 'Event Coefficients with 94% HDI',
    xaxis: { title: 'Event Feature' },
    yaxis: { title: 'Coefficient Value' },
    height: 400,
    margin: { t: 50, b: 50, l: 50, r: 50 },
  });

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Model Analysis
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Bayesian Change Point Detection Results
          </Typography>
        </Box>
        <Box>
          <Button
            variant="contained"
            startIcon={running ? <CircularProgress size={20} /> : <PlayArrow />}
            onClick={runModel}
            disabled={running}
            sx={{ mr: 1 }}
          >
            {running ? 'Running...' : 'Run Model'}
          </Button>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchModelData}
            disabled={running}
          >
            Refresh
          </Button>
        </Box>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Model Status
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Chip
                  label={modelStatus?.models_fitted ? 'Fitted' : 'Not Fitted'}
                  color={modelStatus?.models_fitted ? 'success' : 'warning'}
                  sx={{ mb: 1 }}
                />
              </Box>
              <Typography variant="body2" color="text.secondary">
                Last run: {modelStatus?.last_run || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                WAIC Score (Event Model): {modelStatus?.waic_comparison?.event_waic?.toFixed(2) || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Preferred Model: {modelStatus?.waic_comparison?.preferred_model || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                R-hat Max: {modelStatus?.convergence?.r_hat_max?.toFixed(3) || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                ESS Min: {modelStatus?.convergence?.effective_sample_size_min || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Plot
                data={getPriceSeriesPlotData()}
                layout={getPriceSeriesPlotLayout()}
                style={{ width: '100%', height: '100%' }}
                useResizeHandler={true}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Detected Change Points
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>ID</TableCell>
                      <TableCell>Date</TableCell>
                      <TableCell align="right">Time Index</TableCell>
                      <TableCell>HDI Lower Date</TableCell>
                      <TableCell>HDI Upper Date</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {changePoints?.map((cp) => (
                      <TableRow key={cp.id}>
                        <TableCell>{cp.id}</TableCell>
                        <TableCell>{cp.date}</TableCell>
                        <TableCell align="right">{cp.time_index}</TableCell>
                        <TableCell>{cp.hdi_lower_date}</TableCell>
                        <TableCell>{cp.hdi_upper_date}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Plot
                data={getSegmentCharacteristicsPlotData()}
                layout={getSegmentCharacteristicsPlotLayout()}
                style={{ width: '100%', height: '100%' }}
                useResizeHandler={true}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Plot
                data={getEventCoefficientsPlotData()}
                layout={getEventCoefficientsPlotLayout()}
                style={{ width: '100%', height: '100%' }}
                useResizeHandler={true}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Segment Characteristics (Table)
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Segment ID</TableCell>
                      <TableCell>Start Date</TableCell>
                      <TableCell>End Date</TableCell>
                      <TableCell align="right">Duration (Days)</TableCell>
                      <TableCell align="right">Mean Log Return</TableCell>
                      <TableCell align="right">Volatility</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {segments?.map((segment) => (
                      <TableRow key={segment.id}>
                        <TableCell>{segment.id}</TableCell>
                        <TableCell>{segment.start_date}</TableCell>
                        <TableCell>{segment.end_date}</TableCell>
                        <TableCell align="right">{segment.duration_days}</TableCell>
                        <TableCell align="right">{segment.mean_log_return?.toFixed(5)}</TableCell>
                        <TableCell align="right">{segment.volatility?.toFixed(5)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ModelAnalysis;