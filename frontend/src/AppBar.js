import React from 'react';
import AppBarMaterial from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

import "./appBar.css";

export default function AppBar(props) {
  const {
    setIsNavBarOpen
  } = props;

  return (
    <AppBarMaterial position="static">
      <Toolbar>
        <IconButton edge="start" className="menuButton" color="inherit" onClick={() => setIsNavBarOpen(true)}>
          <MenuIcon />
        </IconButton>
      </Toolbar>
    </AppBarMaterial>
  );
}
