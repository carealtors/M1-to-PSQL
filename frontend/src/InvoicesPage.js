import React, { useState } from 'react';
import { fetchInvoice } from './API'; // Import fetchInvoice
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './App.css';

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
    <div className="invoices-container">
      <button
        onClick={() => navigate('/')} // Navigate back to Home
        className="back-button"
      >
        Back to Home
      </button>
      <h1>Invoices</h1>
      <form onSubmit={handleSubmit} className="invoices-form">
        <label>
          Enter EC Control Number (Ex: 66028047):
          <input
            type="text"
            value={ecControlNumber}
            onChange={(e) => setEcControlNumber(e.target.value)}
            className="input-field"
          />
        </label>
        <button type="submit" className="submit-button">
          Fetch Invoice
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}

      {invoiceData && (
        <div className="invoice-details">
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
