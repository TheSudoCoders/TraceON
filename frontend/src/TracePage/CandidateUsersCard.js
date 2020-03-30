import React from 'react';
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

import './candidateUsersCard.css';

export default function CandidateUsersCard(props) {
  const {
    title,
    isLoading,
    candidates
  } = props;

  let body = <CircularProgress />;
  if (candidates && !isLoading && candidates !== []) {
    body = (
      <>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell align="center">Face Hash</TableCell>
                <TableCell align="center">Interacted on</TableCell>
                <TableCell align="center">Interacted device</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {candidates.map(candidate => (
                <TableRow key={candidate.faceHash}>
                  <TableCell align="center"><Link to={`/tracing/${candidate.faceHash}`}>{candidate.faceHash}</Link></TableCell>
                  <TableCell align="center">{candidate.interactedOn}</TableCell>
                  <TableCell align="center">{candidate.interactedDevice}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </>
    );
  }

  return (
    <Paper className="candidateUsersCard-paper">
      <Typography className="candidateUsersCard-contacts" variant="h2">
        {title}
      </Typography>
      <div className="candidateUsersCard-body">
        {body}
      </div>
    </Paper>
  );
}
