import React, { useState } from 'react';
import { HashRouter, Route } from 'react-router-dom';

import AppBar from './AppBar';
import NavDrawer from './NavDrawer';

import DevicePage from './DevicePage';
import HealthDeclarationPage from './HealthDeclarationPage';
import MapPage from './MapPage';
import TracePage from './TracePage';

import './app.css';

function App() {
  const [isNavBarOpen, setIsNavBarOpen] = useState(false);

  return (
    <HashRouter>
      <div className="app">
        <AppBar setIsNavBarOpen={newValue => setIsNavBarOpen(newValue)} />
        <NavDrawer isOpen={isNavBarOpen} setIsOpen={newValue => setIsNavBarOpen(newValue)} />
        <Route exact path="/">
          <MapPage />
        </Route>

        <Route path="/tracing/:id" render={routeProps => <TracePage {...routeProps} />} />
        <Route path="/device/:id" render={routeProps => <DevicePage {...routeProps} />} />
        <Route path="/declaration" render={routeProps => <HealthDeclarationPage {...routeProps} />} />

      </div>
    </HashRouter >
  );
}

export default App;
