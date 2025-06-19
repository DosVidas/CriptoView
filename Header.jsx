import { Activity, RefreshCw, Wifi, WifiOff } from 'lucide-react';
import { Button } from '@/components/ui/button.jsx';

const Header = ({ lastUpdate, onRefresh, isLoading, isConnected = true }) => {
  const formatLastUpdate = (date) => {
    if (!date) return 'Never';
    
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
      return `${diffInSeconds}s ago`;
    } else if (diffInSeconds < 3600) {
      return `${Math.floor(diffInSeconds / 60)}m ago`;
    } else {
      return date.toLocaleTimeString();
    }
  };

  return (
    <header className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-crypto-blue flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">CriptoView</h1>
                <p className="text-sm text-muted-foreground">
                  Agregador de Precios en Tiempo Real
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              {isConnected ? (
                <Wifi className="w-4 h-4 text-crypto-green" />
              ) : (
                <WifiOff className="w-4 h-4 text-crypto-red" />
              )}
              <span>
                {isConnected ? 'Conectado' : 'Desconectado'}
              </span>
            </div>

            <div className="text-sm text-muted-foreground">
              Última actualización: {formatLastUpdate(lastUpdate)}
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={onRefresh}
              disabled={isLoading}
              className="gap-2"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              Actualizar
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

