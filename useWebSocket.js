import { useState, useEffect } from 'react';
import { useCryptoData } from './useCryptoData';

// Para el MVP, usamos HTTP polling en lugar de WebSockets para simplificar el despliegue
export const useWebSocket = () => {
  const cryptoDataHook = useCryptoData();
  const [isConnected, setIsConnected] = useState(true);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);

  // Simular estado de conexión WebSocket usando el estado del hook HTTP
  useEffect(() => {
    if (cryptoDataHook.error) {
      setIsConnected(false);
      setReconnectAttempts(prev => prev + 1);
    } else {
      setIsConnected(true);
      setReconnectAttempts(0);
    }
  }, [cryptoDataHook.error]);

  const connect = () => {
    cryptoDataHook.refetch();
  };

  const requestData = () => {
    cryptoDataHook.refetch();
  };

  const disconnect = () => {
    // No-op para compatibilidad
  };

  return {
    cryptoData: cryptoDataHook.cryptoData,
    loading: cryptoDataHook.loading,
    error: cryptoDataHook.error,
    lastUpdate: cryptoDataHook.lastUpdate,
    isConnected,
    reconnectAttempts,
    requestData,
    connect,
    disconnect
  };
};

