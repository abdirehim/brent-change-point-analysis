import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
} from '@mui/material';
import { apiService } from '../services/apiService';

const EventAnalysis = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [events, setEvents] = useState(null);
  const [eventCoefficients, setEventCoefficients] = useState(null);
  const [correlations, setCorrelations] = useState(null);

  useEffect(() => {
    const fetchEventData = async () => {
      try {
        setLoading(true);
        const [eventSummary, coefficients, correlationData] = await Promise.all([
          apiService.getEventSummary(),
          apiService.getEventCoefficients(),
          apiService.getCorrelationAnalysis(),
        ]);
        setEvents(eventSummary);
        setEventCoefficients(coefficients);
        setCorrelations(correlationData);
      } catch (err) {
        setError('Failed to load event data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEventData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Event Analysis
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Geopolitical and economic events correlation with Brent oil prices
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Event Summary
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Total Events: {events?.total_events || 'N/A'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Geopolitical: {events?.geopolitical_count || 'N/A'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Economic: {events?.economic_count || 'N/A'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Date Range: {events?.date_range?.start || 'N/A'} to {events?.date_range?.end || 'N/A'}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Event Categories
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {events?.categories?.map((category, index) => (
                  <Chip
                    key={index}
                    label={`${category.name} (${category.count})`}
                    variant="outlined"
                    size="small"
                  />
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Event Impact Coefficients
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Event Type</TableCell>
                      <TableCell align="right">Coefficient</TableCell>
                      <TableCell align="right">HDI Lower</TableCell>
                      <TableCell align="right">HDI Upper</TableCell>
                      <TableCell align="right">Significance</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {eventCoefficients?.map((coef, index) => (
                      <TableRow key={index}>
                        <TableCell>{coef.event_type}</TableCell>
                        <TableCell align="right">{coef.coefficient?.toFixed(4)}</TableCell>
                        <TableCell align="right">{coef.hdi_lower?.toFixed(4)}</TableCell>
                        <TableCell align="right">{coef.hdi_upper?.toFixed(4)}</TableCell>
                        <TableCell align="right">
                          <Chip
                            label={coef.significant ? 'Significant' : 'Not Significant'}
                            color={coef.significant ? 'success' : 'default'}
                            size="small"
                          />
                        </TableCell>
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
              <Typography variant="h6" gutterBottom>
                Recent Events
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Date</TableCell>
                      <TableCell>Event</TableCell>
                      <TableCell>Category</TableCell>
                      <TableCell align="right">Price Impact</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {events?.recent_events?.map((event, index) => (
                      <TableRow key={index}>
                        <TableCell>{event.date}</TableCell>
                        <TableCell>{event.description}</TableCell>
                        <TableCell>
                          <Chip
                            label={event.category}
                            size="small"
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell align="right">
                          {event.price_impact ? `${event.price_impact > 0 ? '+' : ''}${event.price_impact.toFixed(2)}%` : 'N/A'}
                        </TableCell>
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
              <Typography variant="h6" gutterBottom>
                Correlation Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Overall correlation with events: {correlations?.overall_correlation?.toFixed(3) || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Lag effect (days): {correlations?.lag_effect || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Volatility impact: {correlations?.volatility_impact?.toFixed(3) || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default EventAnalysis; 