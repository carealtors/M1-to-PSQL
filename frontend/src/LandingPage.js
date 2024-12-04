import React from 'react';
import { Link } from 'react-router-dom';

function LandingPage() {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      {/* Add the logo */}
      <img 
        src="/CAR-Logo.png" 
        alt="CAR Logo" 

      />
      <h1>CAR Dues Reconciliation Project</h1>
      <nav style={{ marginTop: '30px' }}>
        <Link to="/banks" style={{ marginRight: '20px' }}>Banks</Link>
        <Link to="/invoices">Invoices</Link>
      </nav>
    </div>
  );
}

export default LandingPage;
