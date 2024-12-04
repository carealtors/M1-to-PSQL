import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './LandingPage';
import BanksPage from './BanksPage';
import InvoicesPage from './InvoicesPage';
import DuesLookupPage from './DuesLookupPage'; // Ensure this import is correct

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/banks" element={<BanksPage />} />
          <Route path="/invoices" element={<InvoicesPage />} />
          <Route path="/dues" element={<DuesLookupPage />} /> {/* Ensure this route is defined */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
