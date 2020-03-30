import React, { useState } from 'react';
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
  } = props;

  const [fetching, setFetching] = useState(false);
  const [traceeHasCovid, setTraceeHasCovid] = useState(false);

  //TODO(james): Implement AXIOS to fetch data, probably in useEffect

  let body = null;
  if (fetching) {
    body = <CircularProgress />;
  } else {
    body = (
      <div className="traceCard-TraceeContent">
        <img className="traceCard-TraceeMainImage" src="https://wallpaperaccess.com/full/44753.jpg" />

        {
          traceeHasCovid ?
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
            <GridListTile>
              <img src="https://c4.wallpaperflare.com/wallpaper/641/365/125/portrait-anime-anime-girls-digital-art-artwork-hd-wallpaper-preview.jpg" />
            </GridListTile>
            <GridListTile>
              <img src="https://external-preview.redd.it/x9I6PQkjU2E2hOX66B4ApVfXGYS--PChgBE88Mw36lc.png?auto=webp&s=d577bd668ef73644c0da8578865262129e54e7ec" />
            </GridListTile>
            <GridListTile>
              <img src="https://www.designyourway.net/blog/wp-content/uploads/2017/03/Anime-Wallpaper-Desktop-Background-29-1250x834.jpg" />
            </GridListTile>
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
