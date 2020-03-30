import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Config from '../Config';
import CircularProgress from '@material-ui/core/CircularProgress';
import { Link } from 'react-router-dom';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Typography from '@material-ui/core/Typography';

import './devicePage.css';

export default function DeviceLogTable(props) {
  const {
    match
  } = props;

  const deviceID = match.params['id'];
  const [candidates, setCandidates] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setCandidates([]);
    setIsLoading(true);

    axios.get(Config.backendUrl + Config.paths.device, {
      params: {
        deviceID
      }
    }).then(response => {
      if (response.data && response.data.length > 0) {
        setCandidates(response.data);
        setIsLoading(false);
      }
    });
  }, [deviceID]);

  let body = <CircularProgress />;
  if (!isLoading) {
    body = (
      <>
        <TableContainer className="devicePage-table">
          <Table>
            <TableHead>
              <TableRow>
                <TableCell align="center">Event ID</TableCell>
                <TableCell align="center">Event Last Updated</TableCell>
                <TableCell align="center">Associated Facehash</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {candidates.map(candidate => (
                <TableRow key={candidate.eventID}>
                  <TableCell align="center">{candidate.eventID}</TableCell>
                  <TableCell align="center">{candidate.updatedAt}</TableCell>
                  <TableCell align="center"><Link to={`/tracing/${candidate.faceHash}`}>{candidate.faceHash}</Link></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </>
    );
  }

  return (
    <Paper className="devicePage-paper">
      <Typography className="devicePage-contacts" variant="h2">
        {deviceID}
      </Typography>
      <div className="devicePage-body">
        {body}
      </div>
    </Paper>
  );
}
