import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchExceptions } from './API'; // Import fetchExceptions function

function DuesSummaryPage() {
  const [associations, setAssociations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortConfig, setSortConfig] = useState({ key: 'BillingAssociationID', direction: 'asc' });

  const navigate = useNavigate();

  useEffect(() => {
    fetchExceptions()
      .then((data) => {
        setAssociations(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const sortAssociations = (key) => {
    const direction = sortConfig.key === key && sortConfig.direction === 'asc' ? 'desc' : 'asc';
    setSortConfig({ key, direction });
    setAssociations((prevAssociations) =>
      [...prevAssociations].sort((a, b) => {
        if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
        if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
        return 0;
      })
    );
  };

  if (loading) {
    return <p>Loading dues summary...</p>;
  }

  if (error) {
    return <p style={{ color: 'red' }}>Error: {error}</p>;
  }

  return (
    <div className="dues-summary-container">
      <button className="back-button" onClick={() => navigate('/')}>
        Back to Home
      </button>
      <h1>Dues EC Control Number by Association Summary</h1>
      <table className="dues-summary-table">
        <thead>
          <tr>
            <th onClick={() => sortAssociations('BillingAssociationID')}>Billing Association ID</th>
            <th onClick={() => sortAssociations('AssociationName')}>Association Name</th>
            <th onClick={() => sortAssociations('NullECControlNumber')}>Null EC Control Numbers</th>
            <th onClick={() => sortAssociations('TotalPayments')}>Total Payments</th>
            <th onClick={() => sortAssociations('ECPercentage')}>EC Percentage</th>
          </tr>
        </thead>
        <tbody>
          {associations.map((association) => (
            <tr key={association.BillingAssociationID}>
              <td>{association.BillingAssociationID}</td>
              <td>{association.AssociationName}</td>
              <td>{association.NullECControlNumber}</td>
              <td>{association.TotalPayments}</td>
              <td>{association.ECPercentage}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DuesSummaryPage;
