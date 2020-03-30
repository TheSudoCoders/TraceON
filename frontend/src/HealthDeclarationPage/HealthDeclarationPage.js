import React, { useEffect, useState } from 'react';
import axios from 'axios';
import moment from 'moment';
import Config from '../Config';
import QRCode from 'qrcode.react';
import Box from '@material-ui/core/Box';
import CircularProgress from '@material-ui/core/CircularProgress';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';

import './healthDeclarationPage.css';

// TODO(james): Yup, it looks like this. Sue me.
export default function HealthDeclarationPage(props) {
  const [faceHash, setFaceHash] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    setIsLoading(true);
    setUserInfo(null);

    axios.get(Config.backendUrl + Config.paths.trace, {
      params: {
        faceHash: faceHash,
        startDate: moment.utc().subtract(14, 'days').format(),
        endDate: moment.utc().format()
      }
    }).then(response => {
      const {
        isDirectContact
      } = response.data;

      setUserInfo({ isDirectContact });
    }).finally(() => {
      setIsLoading(false);
    });
  }, [faceHash]);

  let traceOnInformation = (
    <span className="healthDeclarationBox-traceon-invalidHash">
      Cannot find your TraceOn FaceHash. Please input a valid FaceHash!
    </span>
  );

  if (userInfo) {
    traceOnInformation = (
      <span className="healthDeclarationBox-traceon-declare">
        TraceOn FaceHash for this person:
        <br />
        <QRCode value={`${Config.thisUrl}/#/${faceHash}`} />
        <br />
        {
          userInfo.isDirectContact ?
            <span style={{ color: "red" }}>This person may have been in indirect contact with a confirmed case of COVID-19 in the last 14 days.</span>
            :
            `SudoFoundry TraceOn determines that this person has not been in indrect contact with a confirmed case of COVID-19 in the last 14 days.`
        }
      </span>
    );
  }

  if (isLoading) {
    traceOnInformation = (
      <CircularProgress />
    );
  }

  return (
    <Box className="healthDeclarationPage-box">
      <Typography variant="h2">Declaration</Typography>
      I, the holder of the face hash < TextField required id="face-hash" label="Face Hash (16 hex digits)" value={faceHash} onChange={event => setFaceHash(event.target.value)} />, declare that
      towards preventing the spread of Coronavirus Disease 2019(COVID - 19) in our community, have not knowingly come
      into contact with a confirmed COVID - 19 patient, suspected case or person under quarantine in the past 14 days.I
      have also not been to mainland China, and have had a healthy temperature for the past 14 days.

      I declare the information provided by me on the above form to be true and correct to the best of my knowledge and
      belief.

      <Typography variant="h2">SudoFoundry TraceOn</Typography>
      {traceOnInformation}
    </Box >
  );
}
