import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  Box,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  DataUsage as DataIcon,
  ModelTraining as ModelIcon,
  Event as EventIcon,
  Assessment as ReportsIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Data Explorer', icon: <DataIcon />, path: '/data' },
  { text: 'Model Analysis', icon: <ModelIcon />, path: '/model' },
  { text: 'Event Analysis', icon: <EventIcon />, path: '/events' },
  { text: 'Reports', icon: <ReportsIcon />, path: '/reports' },
];

const Sidebar = ({ open, onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (path) => {
    navigate(path);
    if (window.innerWidth < 600) {
      onClose();
    }
  };

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          top: 64,
          height: 'calc(100% - 64px)',
        },
      }}
    >
      <Box sx={{ overflow: 'auto' }}>
        <List>
          {menuItems.map((item, index) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => handleNavigation(item.path)}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
        <Divider />
        <Box sx={{ p: 2 }}>
          <Box sx={{ fontSize: '0.75rem', color: 'text.secondary' }}>
            Brent Oil Price Analysis
          </Box>
          <Box sx={{ fontSize: '0.75rem', color: 'text.secondary' }}>
            Bayesian Change Point Detection
          </Box>
        </Box>
      </Box>
    </Drawer>
  );
};

export default Sidebar; 