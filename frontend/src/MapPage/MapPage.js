import React from 'react';
import { Link } from 'react-router-dom';
import { Map, Marker, Popup, TileLayer } from 'react-leaflet';
import Leaflet from 'leaflet/dist/leaflet.js';

import mainIcon from 'leaflet/dist/images/marker-icon.png';
import shadowIcon from 'leaflet/dist/images/marker-shadow.png';
import 'leaflet/dist/leaflet.css';

import './mapPage.css';

/**
   Note: In this scenario, we're focusing on Singapore. Hence, the coordinates here are hard-coded.
   In a different approach, each portal user would have a different starting coordinate, and would not
   have to rely on a hardcoded coordiante.
*/
const MapPage = props => {
  // HACK(james): Apparently things don't render right. No idea why. So I did this to bypass all the shenanigan
  const icon = Leaflet.icon({
    iconUrl: mainIcon,
    shadowUrl: shadowIcon,
  });

  // HACK(james): Hardcode marker positions and device IDs too. Faster to demonstrate the concept
  return (
    <Map center={[1.351616, 103.808053]} zoom={12.3}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; <a href=&quot;https://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
      />

      <Marker position={[1.351616, 103.808053]} icon={icon}>
        <Popup>
          Device: <Link to={`/device/56df4a2141844a70b4c91df2ee58e5f7`}>56df4a2141844a70b4c91df2ee58e5f7</Link>
        </Popup>
      </Marker>
    </Map>
  );
};

export default MapPage;
