import { useState, useEffect } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import Header from './components/Header';
import CryptoCard from './components/CryptoCard';
import LoadingSkeleton from './components/LoadingSkeleton';
import ErrorState from './components/ErrorState';
import './App.css';

function App() {
  const { 
    cryptoData, 
    loading, 
    error, 
    lastUpdate, 
    isConnected, 
    reconnectAttempts,
    requestData,
    connect 
  } = useWebSocket();
  
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  // Monitor connection status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const handleRefresh = () => {
    if (isConnected) {
      requestData();
    } else {
      connect();
    }
  };

  const connectionStatus = isOnline && isConnected;

  return (
    <div className="min-h-screen bg-background">
      <Header
        lastUpdate={lastUpdate}
        onRefresh={handleRefresh}
        isLoading={loading}
        isConnected={connectionStatus}
      />

      <main className="container mx-auto px-4 py-8">
        {error && !isConnected ? (
          <ErrorState 
            error={`${error}${reconnectAttempts > 0 ? ` (Intentos de reconexión: ${reconnectAttempts})` : ''}`} 
            onRetry={handleRefresh} 
          />
        ) : (
          <>
            <div className="mb-8">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold mb-2">
                    Precios de Criptomonedas en Tiempo Real
                  </h2>
                  <p className="text-muted-foreground">
                    Datos agregados desde múltiples exchanges: Binance, Coinbase y KuCoin
                  </p>
                </div>
                
                <div className="flex items-center gap-4">
                  {!connectionStatus && (
                    <div className="text-sm text-crypto-red">
                      {!isOnline ? 'Sin conexión a internet' : 'Conectando...'}
                    </div>
                  )}
                  
                  {isConnected && (
                    <div className="flex items-center gap-2 text-sm text-crypto-green">
                      <div className="w-2 h-2 bg-crypto-green rounded-full animate-pulse"></div>
                      Tiempo real activo
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {loading && cryptoData.length === 0 ? (
                // Show loading skeletons on initial load
                Array.from({ length: 12 }).map((_, index) => (
                  <LoadingSkeleton key={index} />
                ))
              ) : (
                // Show crypto cards
                cryptoData.map((crypto) => (
                  <CryptoCard key={crypto.symbol} crypto={crypto} />
                ))
              )}
            </div>

            {cryptoData.length === 0 && !loading && !error && (
              <div className="text-center py-12">
                <p className="text-muted-foreground">
                  No hay datos de criptomonedas disponibles en este momento.
                </p>
              </div>
            )}
          </>
        )}
      </main>

      <footer className="border-t border-border mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="font-semibold mb-3">Fuentes de Datos</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Binance API</li>
                <li>• Coinbase Exchange API</li>
                <li>• KuCoin API</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-3">Información</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Actualizaciones en tiempo real vía WebSocket</li>
                <li>• Datos agregados de múltiples fuentes</li>
                <li>• Reconexión automática</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-3">Disclaimer</h3>
              <p className="text-sm text-muted-foreground">
                Los precios mostrados son solo para fines informativos. 
                No constituyen asesoramiento financiero.
              </p>
            </div>
          </div>
          
          <div className="border-t border-border mt-8 pt-8 text-center">
            <p className="text-sm text-muted-foreground">
              © 2025 CriptoView. Desarrollado como MVP para agregación de precios de criptomonedas.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;

