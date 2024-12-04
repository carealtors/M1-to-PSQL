import React, { useEffect, useState } from 'react';
import { fetchBanks } from './API';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchBanks().then((data) => setData(data));
  }, []);

  return (
    <div>
      <h1>React Frontend</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default App;
