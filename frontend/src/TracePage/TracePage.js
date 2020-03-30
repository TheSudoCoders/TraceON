import React, { useState } from 'react';
import axios from 'axios';
import Paper from '@material-ui/core/Paper';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from '@material-ui/core/Typography';

import TraceeCard from './TraceeCard';

import './tracePage.css';

export default function TracePage(props) {
  const {
    match,
  } = props;

  const faceHash = match.params['id'];
  return (
    <div className="tracePage-div">
      <TraceeCard faceHash={faceHash} />
    </div>
  );
}
