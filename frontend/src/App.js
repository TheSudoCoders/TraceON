import React, { useState } from 'react';
import { HashRouter, Route } from 'react-router-dom';

import AppBar from './AppBar';
import NavDrawer from './NavDrawer';

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
      </div>
    </HashRouter >
  );
}

export default App;
