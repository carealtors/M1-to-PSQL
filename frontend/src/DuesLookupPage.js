import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchDues } from './API'; // Import fetchDues from API.js

function DuesLookupPage() {
  const [memberId, setMemberId] = useState('');
  const [billingYear, setBillingYear] = useState(2024); // Default year
  const [duesData, setDuesData] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Generate years from 2015 to 2023, and include 2024 by default
  const pastYears = Array.from({ length: 9 }, (_, i) => 2015 + i); // Years from 2015 to 2023
  const futureYears = Array.from({ length: 6 }, (_, i) => 2025 + i); // Years from 2025 to 2030
  const years = [...pastYears, 2024, ...futureYears]; // Combine past, present, and future years


  const handleSubmit = async (event) => {
    event.preventDefault();
    if (memberId) {
      try {
        const data = await fetchDues(memberId, billingYear); // Use fetchDues
        setDuesData(data);
        setError(null);
      } catch (err) {
        setDuesData(null);
        setError(err.message);
      }
    } else {
      setError('Please enter a valid Member ID.');
    }
  };

  return (
    <div className="dues-lookup-container">
      <button
        onClick={() => navigate('/')}
        className="back-button"
      >
        Back to Home
      </button>
      <h1>Dues Lookup</h1>
      <form onSubmit={handleSubmit} className="dues-lookup-form">
  <div className="form-group">
    <label>
      Member ID:
      <input
        type="text"
        value={memberId}
        onChange={(e) => setMemberId(e.target.value)}
        className="input-field"
      />
    </label>
  </div>
  <div className="form-group">
    <label>
      Billing Year:
      <select
        value={billingYear}
        onChange={(e) => setBillingYear(Number(e.target.value))}
        className="dropdown"
      >
        {years.map((year) => (
          <option key={year} value={year}>
            {year}
          </option>
        ))}
      </select>
    </label>
  </div>
  <button type="submit" className="submit-button">
    Lookup Dues
  </button>
</form>

      {error && <p className="error-message">{error}</p>}

      {duesData && (
        <div className="dues-details">
          <h2>Dues Details</h2>
          <p><strong>Member ID:</strong> {duesData.MemberID}</p>
          <p><strong>Member Name:</strong> {duesData.MemberName}</p>
          <p><strong>Billing Year:</strong> {duesData.BillingYear}</p>
          <p><strong>Amount:</strong> ${duesData.Amount}</p>
          <p><strong>Status:</strong> {duesData.Status}</p>
        </div>
      )}
    </div>
  );
}

export default DuesLookupPage;
