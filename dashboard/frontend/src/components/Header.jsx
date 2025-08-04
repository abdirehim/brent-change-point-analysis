import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Chip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material';

const Header = ({ onMenuClick }) => {
  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
      }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={onMenuClick}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
        <AnalyticsIcon sx={{ mr: 2 }} />
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          Brent Change Point Analysis
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Chip label="Live" color="success" size="small" />
          <Chip label="v1.0.0" variant="outlined" size="small" />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 