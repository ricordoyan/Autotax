import React, { useEffect, useState } from 'react';
import { initTaxReturn, createTaxReturn } from '../services/taxService';

const TaxReturn = () => {
  const [error, setError] = useState(null);

  useEffect(() => {
    const initializeTaxReturn = async () => {
      try {
        await initTaxReturn();
      } catch (error) {
        setError(error.message);
        console.error('Failed to initialize tax return:', error);
      }
    };

    initializeTaxReturn();
  }, []);

  // Rest of your component code...

  return (
    <div>
      {error && (
        <div style={{ color: 'red', padding: '10px' }}>
          Error: {error}
        </div>
      )}
      {/* Rest of your component JSX */}
    </div>
  );
};

export default TaxReturn; 