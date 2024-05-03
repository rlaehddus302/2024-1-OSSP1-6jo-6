import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Welcomepage from './ICU/Welcome/src/App';
import Loginpage from './ICU/Login/src/App';
import Signuppage from './ICU/signUp/src/App';
import CCTVpage from './ICU/CCTV/src/App';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcomepage />} />
        <Route path="/login" element={<Loginpage />} />
        <Route path="/signUp" element={<Signuppage />} />
        <Route path="/cctv" element={<CCTVpage />} />
      </Routes>
    </Router>
  );
}

export default App;
