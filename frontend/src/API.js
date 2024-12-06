const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === 'development'
    ? 'http://localhost:5001'
    : 'http://api:5000');

export async function fetchBanks() {
  const response = await fetch(`${API_BASE_URL}/banks/`);
  if (!response.ok) {
    throw new Error(`Error fetching banks: ${response.statusText}`);
  }
  const data = await response.json();
  return data;
}

export async function fetchInvoice(ecControlNumber) {
  const response = await fetch(`${API_BASE_URL}/invoices/${ecControlNumber}`);
  if (!response.ok) {
    throw new Error(`Error fetching invoice: ${response.statusText}`);
  }
  const data = await response.json();
  return data;
}

export async function fetchDues(memberId, year) {
    const response = await fetch(`${API_BASE_URL}/dues/${memberId}/${year}`);
    if (!response.ok) {
      throw new Error(`Error fetching dues for Member ID: ${memberId} in ${year}`);
    }
    return await response.json();
  }

  export async function fetchExceptions() {
    const response = await fetch(`${API_BASE_URL}/dues_summary/`);
    if (!response.ok) {
      throw new Error(`Error fetching dues summaries and exceptions: ${response.statusText}`);
    }
    return await response.json();
  } 