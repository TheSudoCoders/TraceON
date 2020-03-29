import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core';

const useStyles = makeStyles(themes => ({

}));

export default function() {
  const classes = useStyles();

  return (
    <AppBar position='static'>
      <Toolbar>
      </Toolbar>
    </AppBar>
  );
}
