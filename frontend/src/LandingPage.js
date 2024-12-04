import React from 'react';
import { Link } from 'react-router-dom';
import './App.css'; // Make sure to import your CSS file

function LandingPage() {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <img 
        src="/CAR-Logo.svg" 
        alt="CAR Logo" 
        className="logo" // Add class to the logo image
      />
      <h1>Dues Reconciliation Project</h1>
      <nav style={{ marginTop: '30px' }}>
        <Link to="/banks" style={{ marginRight: '20px' }}>Banks</Link>
        <Link to="/invoices" style={{ marginRight: '20px' }}>Invoices</Link>
        <Link to="/dues">Dues Lookup</Link> {/* Added Link */}
      </nav>
    </div>
  );
}

export default LandingPage;
