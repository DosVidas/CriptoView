import { AlertCircle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button.jsx';

const ErrorState = ({ error, onRetry }) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
      <div className="w-16 h-16 rounded-full bg-destructive/10 flex items-center justify-center mb-4">
        <AlertCircle className="w-8 h-8 text-destructive" />
      </div>
      
      <h3 className="text-xl font-semibold mb-2">Error al cargar datos</h3>
      
      <p className="text-muted-foreground mb-6 max-w-md">
        No se pudieron obtener los precios de las criptomonedas. 
        Verifica tu conexión a internet e inténtalo de nuevo.
      </p>
      
      <div className="text-sm text-muted-foreground mb-4 p-3 bg-muted rounded-lg">
        <strong>Error:</strong> {error}
      </div>
      
      <Button onClick={onRetry} className="gap-2">
        <RefreshCw className="w-4 h-4" />
        Reintentar
      </Button>
    </div>
  );
};

export default ErrorState;

