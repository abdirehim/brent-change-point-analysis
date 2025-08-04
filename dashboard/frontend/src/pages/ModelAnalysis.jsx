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

const ModelAnalysis = () => {
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState(null);
  const [modelStatus, setModelStatus] = useState(null);
  const [changePoints, setChangePoints] = useState(null);
  const [segments, setSegments] = useState(null);

  useEffect(() => {
    fetchModelData();
  }, []);

  const fetchModelData = async () => {
    try {
      setLoading(true);
      const [status, changepoints, segmentData] = await Promise.all([
        apiService.getModelStatus(),
        apiService.getChangePoints(),
        apiService.getSegments(),
      ]);
      setModelStatus(status);
      setChangePoints(changepoints);
      setSegments(segmentData);
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
                  label={modelStatus?.status || 'Unknown'}
                  color={modelStatus?.status === 'ready' ? 'success' : 'warning'}
                  sx={{ mb: 1 }}
                />
              </Box>
              <Typography variant="body2" color="text.secondary">
                Last run: {modelStatus?.last_run || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                WAIC Score: {modelStatus?.waic_score || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Convergence: {modelStatus?.convergence || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Detected Change Points
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Date</TableCell>
                      <TableCell align="right">Probability</TableCell>
                      <TableCell align="right">HDI Lower</TableCell>
                      <TableCell align="right">HDI Upper</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {changePoints?.map((cp, index) => (
                      <TableRow key={index}>
                        <TableCell>{cp.date}</TableCell>
                        <TableCell align="right">{(cp.probability * 100).toFixed(1)}%</TableCell>
                        <TableCell align="right">{cp.hdi_lower}</TableCell>
                        <TableCell align="right">{cp.hdi_upper}</TableCell>
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
                Segment Characteristics
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Segment</TableCell>
                      <TableCell align="right">Start Date</TableCell>
                      <TableCell align="right">End Date</TableCell>
                      <TableCell align="right">Mean Price</TableCell>
                      <TableCell align="right">Volatility</TableCell>
                      <TableCell align="right">Trend</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {segments?.map((segment, index) => (
                      <TableRow key={index}>
                        <TableCell>Segment {index + 1}</TableCell>
                        <TableCell align="right">{segment.start_date}</TableCell>
                        <TableCell align="right">{segment.end_date}</TableCell>
                        <TableCell align="right">${segment.mean_price?.toFixed(2)}</TableCell>
                        <TableCell align="right">{segment.volatility?.toFixed(3)}</TableCell>
                        <TableCell align="right">
                          <Chip
                            label={segment.trend}
                            color={segment.trend === 'increasing' ? 'success' : 'error'}
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
      </Grid>
    </Box>
  );
};

export default ModelAnalysis; 