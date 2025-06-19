import { useState, useEffect } from 'react';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://58hpi8clzdm5.manus.space/api' 
  : 'http://localhost:5001/api';

export const useCryptoData = () => {
  const [cryptoData, setCryptoData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  const fetchCryptoData = async () => {
    try {
      setError(null);
      const response = await fetch(`${API_BASE_URL}/crypto/prices`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.success) {
        setCryptoData(data.data);
        setLastUpdate(new Date(data.timestamp * 1000));
      } else {
        throw new Error(data.error || 'Failed to fetch crypto data');
      }
    } catch (err) {
      setError(err.message);
      console.error('Error fetching crypto data:', err);
    } finally {
      setLoading(false);
    }
  };

  const startPeriodicUpdates = async () => {
    try {
      await fetch(`${API_BASE_URL}/crypto/start-updates`, {
        method: 'POST',
      });
    } catch (err) {
      console.error('Error starting periodic updates:', err);
    }
  };

  useEffect(() => {
    fetchCryptoData();
    startPeriodicUpdates();

    // Set up periodic fetching every 10 seconds
    const interval = setInterval(fetchCryptoData, 10000);

    return () => clearInterval(interval);
  }, []);

  return {
    cryptoData,
    loading,
    error,
    lastUpdate,
    refetch: fetchCryptoData
  };
};

