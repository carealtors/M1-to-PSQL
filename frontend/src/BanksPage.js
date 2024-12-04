import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { fetchBanks } from './API';

function BanksPage() {
  const [banks, setBanks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize navigate

  useEffect(() => {
    fetchBanks()
      .then((data) => {
        const sortedBanks = data.sort((a, b) => a.BankID - b.BankID);
        setBanks(sortedBanks);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading banks...</p>;
  }

  if (error) {
    return <p style={{ color: 'red' }}>Error: {error}</p>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <button
        onClick={() => navigate('/')} // Navigate to Landing Page
        style={{
          marginBottom: '20px',
          padding: '10px 20px',
          backgroundColor: '#007bff',
          color: '#fff',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        Back to Home
      </button>
      <h1>Banks</h1>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Bank ID</th>
            <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Name</th>
          </tr>
        </thead>
        <tbody>
          {banks.map((bank) => (
            <tr key={bank.BankID}>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{bank.BankID}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{bank.BankName}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BanksPage;
