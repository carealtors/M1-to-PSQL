import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './LandingPage';
import BanksPage from './BanksPage';
import InvoicesPage from './InvoicesPage';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/banks" element={<BanksPage />} />
          <Route path="/invoices" element={<InvoicesPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
