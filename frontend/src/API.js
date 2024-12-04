const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === "development"
    ? "http://localhost:5001"
    : "http://api:5000");

export async function fetchBanks() { // Renamed to fetchData
  const response = await fetch(`${API_BASE_URL}/banks/`);
  if (!response.ok) {
    throw new Error(`Error fetching banks: ${response.statusText}`);
  }
  const data = await response.json();
  return data;
}
