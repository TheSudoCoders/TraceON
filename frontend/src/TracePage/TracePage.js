import React, { useState, useEffect } from 'react';
import axios from 'axios';
import moment from 'moment';

import Config from '../Config';
import CandidateLists from './CandidateLists';
import TraceeCard from './TraceeCard';

import './tracePage.css';

export default function TracePage(props) {
  const {
    match,
  } = props;

  const faceHash = match.params['id'];
  const [fetching, setFetching] = useState(true);
  const [candidates, setCandidates] = useState([]);
  const [images, setImages] = useState([]);
  const [traceeHasCovid, setTraceeHasCovid] = useState(false);

  useEffect(() => {
    setFetching(true);
    setCandidates([]);
    setImages([]);
    setTraceeHasCovid(false);

    axios.get(Config.backendUrl + Config.paths.trace, {
      params: {
        faceHash: faceHash,
        startDate: moment.utc().subtract(14, 'days').format(),
        endDate: moment.utc().format()
      }
    }).then(response => {
      const {
        tracees,
        isDirectContact
      } = response.data;
      setFetching(false);
      setCandidates(tracees);
      setTraceeHasCovid(isDirectContact);
    });

    axios.get(Config.backendUrl + Config.paths.images, {
      params: {
        faceHash: faceHash
      }
    }).then(response => {
      const image_url_array = response.data;
      if (image_url_array && image_url_array !== []) {
        setImages(image_url_array);
      }
    });
  }, [faceHash]);

  return (
    <div className="tracePage-div">
      <TraceeCard
        faceHash={faceHash}
        isLoading={fetching}
        personHasCovid={traceeHasCovid}
        imageUrls={images}
      />
      <CandidateLists candidates={candidates} isLoading={fetching} />
    </div>
  );
}
