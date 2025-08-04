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
} from '@mui/material';
import { apiService } from '../services/apiService';

const DataExplorer = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [priceData, setPriceData] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [priceSeries, dataSummary] = await Promise.all([
          apiService.getPriceSeries(),
          apiService.getDataSummary(),
        ]);
        setPriceData(priceSeries);
        setStats(dataSummary);
      } catch (err) {
        setError('Failed to load data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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
        Data Explorer
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Explore Brent oil price data and statistics
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Data Summary
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableBody>
                    <TableRow>
                      <TableCell><strong>Total Observations</strong></TableCell>
                      <TableCell>{stats?.data_points || 'N/A'}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Date Range</strong></TableCell>
                      <TableCell>
                        {stats?.date_range?.start || 'N/A'} to {stats?.date_range?.end || 'N/A'}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Min Price</strong></TableCell>
                      <TableCell>${stats?.price_range?.min || 'N/A'}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Max Price</strong></TableCell>
                      <TableCell>${stats?.price_range?.max || 'N/A'}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Mean Price</strong></TableCell>
                      <TableCell>${stats?.price_stats?.mean || 'N/A'}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Std Deviation</strong></TableCell>
                      <TableCell>${stats?.price_stats?.std || 'N/A'}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Price Data
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Date</TableCell>
                      <TableCell align="right">Price (USD)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {priceData?.slice(-10).map((row, index) => (
                      <TableRow key={index}>
                        <TableCell>{row.date}</TableCell>
                        <TableCell align="right">${row.price?.toFixed(2)}</TableCell>
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
                Data Quality
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Missing values: {stats?.missing_values || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Data completeness: {stats?.completeness || 'N/A'}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Last updated: {stats?.last_updated || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DataExplorer; 