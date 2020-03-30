import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Paper from '@material-ui/core/Paper';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from '@material-ui/core/Typography';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';

import './traceeCard.css';

export default function TraceeCard(props) {
  const {
    faceHash,
    isLoading,
    imageUrls,
    personHasCovid
  } = props;

  //TODO(james): Implement "successful" sequence main imaging. Need changes to API.
  const [currentImage, setCurrentImage] = useState(null);
  useEffect(() => {
    if (imageUrls.length >= 1) {
      setCurrentImage(imageUrls[0]);
    }
  }, [imageUrls]);

  let body = null;
  if (isLoading || imageUrls.length === 0) {
    body = <CircularProgress />;
  } else {
    body = (
      <div className="traceCard-TraceeContent">
        <img className="traceCard-TraceeMainImage" src={currentImage} />

        {
          personHasCovid ?
            <Typography variant="h5">
              <span style={{ color: 'red' }}>This person <i>may</i> have the COVID-19 disease.</span>
            </Typography>
            :
            <Typography variant="h5">
              <span style={{ color: 'green' }}>This person is safe</span>
            </Typography>
        }

        <div className="traceCard-imageList">
          <GridList className="traceCard-TraceeImages" cols={2.5}>
            {imageUrls.map(imageUrl => (
              <GridListTile key={imageUrl} onClick={() => setCurrentImage(imageUrl)}>
                <img src={imageUrl} />
              </GridListTile>
            ))}
          </GridList>
        </div>
      </div>
    );
  }

  return (
    <div className="traceCard-div">
      <Paper className="traceCard-TraceePaper">
        <Typography variant="h3">
          {faceHash}
        </Typography>
        <div className="traceCard-TraceeBody">
          {body}
        </div>
      </Paper>
    </div>
  );
}
