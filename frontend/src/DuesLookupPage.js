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

  // Helper function to format the Last Changed date without milliseconds
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toISOString().slice(0, 19).replace('T', ' '); // Remove milliseconds and reformat to YYYY-MM-DD HH:mm:ss
  };

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
            Member ID (Ex: 198511187):
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
          <table className="dues-table">
            <thead>
              <tr>
                <th>Member Name</th>
                <th>Billing Year</th>
                <th>Payment Amount</th>
                <th>Dues Paid Date</th>
                <th>EC Control Number</th>
                <th>Payment Type</th>
                <th>Last Changed</th>
              </tr>
            </thead>
            <tbody>
              {duesData.map((duesEntry, index) => (
                <tr key={index}>
                  <td>{duesEntry.MEMBER_FIRST_NAME} {duesEntry.MEMBER_LAST_NAME}</td>
                  <td>{duesEntry.BILLING_YEAR}</td>
                  <td>${duesEntry.PAYMENT_AMOUNT}</td>
                  <td>{duesEntry.DUES_PAID_DATE}</td>
                  <td>{duesEntry.EC_CONTROL_NUMBER}</td>
                  <td>{duesEntry.PAYMENT_TYPE_CODE}</td>
                  <td>{formatDate(duesEntry.LAST_CHANGED_DATETIME)}</td> {/* Format the date */}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default DuesLookupPage;
