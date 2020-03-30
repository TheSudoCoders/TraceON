import React, { useState, useEffect } from 'react';
import { Redirect } from 'react-router-dom';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';

import HomeIcon from '@material-ui/icons/Home';
import LocalHospitalIcon from '@material-ui/icons/LocalHospital';

import './navDrawer.css';

export default function NavDrawer(props) {
  const {
    isOpen,
    setIsOpen
  } = props;

  const [redirectComponent, setRedirectComponent] = useState(null);
  useEffect(() => {
    setRedirectComponent(null);
  }, [isOpen]);

  return (
    <Drawer
      anchor="left"
      open={isOpen}
      onClose={() => setIsOpen(false)}
    >
      {redirectComponent}
      <List className="navDrawer">
        <ListItem button key="Home" onClick={() => {
          setRedirectComponent(<Redirect to="/"></Redirect>);
          setIsOpen(false);
        }}>
          <ListItemIcon><HomeIcon /></ListItemIcon>
          <ListItemText>Home</ListItemText>
        </ListItem>
        <ListItem button key="Declaration" onClick={() => {
          setRedirectComponent(<Redirect to="/declaration"></Redirect>);
          setIsOpen(false);
        }}>
          <ListItemIcon><LocalHospitalIcon /></ListItemIcon>
          <ListItemText>Health Declaration</ListItemText>
        </ListItem>
      </List>
    </Drawer>
  );
}
