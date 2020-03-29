import React from 'react';

import { BrowserRouter } from 'react-router-dom';
import AppBar from './AppBar';

function App() {
  return (
    <BrowserRouter>
      <AppBar position="static">
      </AppBar>
    </BrowserRouter >
  );
}

export default App;
