import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Chip,
} from '@mui/material';
import {
  Description,
  PictureAsPdf,
  Slideshow,
  Download,
  Visibility,
} from '@mui/icons-material';

const Reports = () => {
  const [reports] = useState([
    {
      id: 1,
      title: 'Interim Analysis Report',
      type: 'PDF',
      description: 'Preliminary findings from Bayesian change point analysis',
      date: '2024-01-15',
      status: 'completed',
      file: 'interim_report.pdf',
    },
    {
      id: 2,
      title: 'Final Analysis Report',
      type: 'PDF',
      description: 'Comprehensive analysis with event correlation findings',
      date: '2024-02-01',
      status: 'completed',
      file: 'final_report.pdf',
    },
    {
      id: 3,
      title: 'Executive Summary Presentation',
      type: 'PPTX',
      description: 'Key findings and insights for stakeholders',
      date: '2024-02-01',
      status: 'completed',
      file: 'summary_slide_deck.pptx',
    },
    {
      id: 4,
      title: 'Technical Methodology Report',
      type: 'PDF',
      description: 'Detailed methodology and model specifications',
      date: '2024-01-20',
      status: 'completed',
      file: 'technical_methodology.pdf',
    },
  ]);

  const handleDownload = (file) => {
    // In a real application, this would trigger a download
    console.log(`Downloading ${file}`);
    alert(`Download started for ${file}`);
  };

  const handleView = (file) => {
    // In a real application, this would open the file in a viewer
    console.log(`Viewing ${file}`);
    alert(`Opening ${file} in viewer`);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'in_progress':
        return 'warning';
      case 'pending':
        return 'default';
      default:
        return 'default';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'PDF':
        return <PictureAsPdf />;
      case 'PPTX':
        return <Slideshow />;
      default:
        return <Description />;
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Reports & Presentations
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Analysis reports and presentation materials
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Available Reports
              </Typography>
              <List>
                {reports.map((report, index) => (
                  <React.Fragment key={report.id}>
                    <ListItem>
                      <ListItemIcon>
                        {getTypeIcon(report.type)}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box display="flex" alignItems="center" gap={1}>
                            {report.title}
                            <Chip
                              label={report.status}
                              color={getStatusColor(report.status)}
                              size="small"
                            />
                          </Box>
                        }
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {report.description}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              Generated: {report.date}
                            </Typography>
                          </Box>
                        }
                      />
                      <Box>
                        <Button
                          size="small"
                          startIcon={<Visibility />}
                          onClick={() => handleView(report.file)}
                          sx={{ mr: 1 }}
                        >
                          View
                        </Button>
                        <Button
                          size="small"
                          variant="outlined"
                          startIcon={<Download />}
                          onClick={() => handleDownload(report.file)}
                        >
                          Download
                        </Button>
                      </Box>
                    </ListItem>
                    {index < reports.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Report Summary
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Total Reports: {reports.length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  PDF Reports: {reports.filter(r => r.type === 'PDF').length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Presentations: {reports.filter(r => r.type === 'PPTX').length}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Latest Update: {reports[0]?.date || 'N/A'}
              </Typography>
            </CardContent>
          </Card>

          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Report Types
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Box>
                  <Typography variant="body2" fontWeight="bold">
                    Interim Report
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Preliminary findings and initial model results
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" fontWeight="bold">
                    Final Report
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Complete analysis with all findings and conclusions
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" fontWeight="bold">
                    Executive Summary
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    High-level insights for decision makers
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" fontWeight="bold">
                    Technical Report
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Detailed methodology and technical specifications
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Reports; 