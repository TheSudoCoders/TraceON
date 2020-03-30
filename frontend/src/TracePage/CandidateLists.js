import React from 'react';

import CandidateUsersCard from './CandidateUsersCard';

import './candidateLists.css';

export default function CandidateLists(props) {
  const {
    candidates,
    isLoading,
  } = props;

  const badTouchCandidates = candidates.filter(candidate => candidate.isConfirmedCase);

  return (
    <div className="candidateLists-div">
      <CandidateUsersCard title="Contacts" candidates={candidates} isLoading={isLoading} />
      <CandidateUsersCard title="Bad Touch" candidates={badTouchCandidates} isLoading={isLoading} />
    </div>
  );
}
