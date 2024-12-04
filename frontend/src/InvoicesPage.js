import React, { useState } from 'react';
import { fetchInvoice } from './API'; // Import fetchInvoice
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function InvoicesPage() {
  const [ecControlNumber, setEcControlNumber] = useState('');
  const [invoiceData, setInvoiceData] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize navigate

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (ecControlNumber) {
      try {
        const data = await fetchInvoice(ecControlNumber); // Use fetchInvoice
        setInvoiceData(data);
        setError(null);
      } catch (err) {
        setInvoiceData(null);
        setError(err.message);
      }
    } else {
      setError('Please enter a valid EC Control Number.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <button
        onClick={() => navigate('/')} // Navigate back to Home
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
      <h1>Invoices</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <label>
          Enter EC Control Number:
          <input
            type="text"
            value={ecControlNumber}
            onChange={(e) => setEcControlNumber(e.target.value)}
            style={{
              marginLeft: '10px',
              padding: '5px',
              border: '1px solid #ddd',
              borderRadius: '4px',
            }}
          />
        </label>
        <button
          type="submit"
          style={{
            marginLeft: '10px',
            padding: '5px 10px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Fetch Invoice
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {invoiceData && (
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '4px' }}>
          <h2>Invoice Details</h2>
          <p><strong>ACH Settlement Number:</strong> {invoiceData.ACHSettlementNumber}</p>
          <p><strong>Association Portion:</strong> ${invoiceData.AssociationPortion}</p>
          <p><strong>Bank ID:</strong> {invoiceData.BankID}</p>
          <p><strong>Billing Year:</strong> {invoiceData.BillingYear}</p>
          <p><strong>Destination Association:</strong> {invoiceData.DestinationAssociation}</p>
          <p><strong>EC Control Number:</strong> {invoiceData.ECControlNumber}</p>
          <p><strong>Gross Amount:</strong> ${invoiceData.GrossAmount}</p>
          <p><strong>Invoice ID:</strong> {invoiceData.InvoiceID}</p>
          <p><strong>Member ID:</strong> {invoiceData.MemberID}</p>
          <p><strong>Member Name:</strong> {invoiceData.MemberName}</p>
          <p><strong>Net Association Portion:</strong> ${invoiceData.NetAssociationPortion}</p>
          <p><strong>Transaction Fee:</strong> ${invoiceData.TransactionFee}</p>
        </div>
      )}
    </div>
  );
}

export default InvoicesPage;
