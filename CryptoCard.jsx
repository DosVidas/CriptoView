import { TrendingUp, TrendingDown } from 'lucide-react';

const CryptoIcon = ({ symbol, className = "" }) => {
  const getIconStyle = (symbol) => {
    const iconStyles = {
      'BTC': { bg: 'bg-orange-500', text: '₿' },
      'ETH': { bg: 'bg-blue-500', text: 'Ξ' },
      'BNB': { bg: 'bg-yellow-500', text: 'B' },
      'XRP': { bg: 'bg-blue-600', text: 'X' },
      'ADA': { bg: 'bg-blue-700', text: 'A' },
      'SOL': { bg: 'bg-purple-500', text: 'S' },
      'DOGE': { bg: 'bg-yellow-600', text: 'D' },
      'DOT': { bg: 'bg-pink-500', text: '●' },
      'MATIC': { bg: 'bg-purple-600', text: 'M' },
      'LTC': { bg: 'bg-gray-500', text: 'Ł' },
      'SHIB': { bg: 'bg-orange-600', text: 'S' },
      'TRX': { bg: 'bg-red-500', text: 'T' },
      'AVAX': { bg: 'bg-red-600', text: 'A' },
      'UNI': { bg: 'bg-pink-600', text: 'U' },
      'ATOM': { bg: 'bg-blue-800', text: 'A' },
      'LINK': { bg: 'bg-blue-400', text: 'L' },
      'XMR': { bg: 'bg-orange-700', text: 'M' },
      'ETC': { bg: 'bg-green-600', text: 'E' },
      'BCH': { bg: 'bg-green-500', text: 'B' },
      'NEAR': { bg: 'bg-green-400', text: 'N' },
      'APT': { bg: 'bg-blue-300', text: 'A' },
      'QNT': { bg: 'bg-gray-600', text: 'Q' },
      'ICP': { bg: 'bg-purple-700', text: 'I' },
      'FIL': { bg: 'bg-blue-900', text: 'F' },
      'VET': { bg: 'bg-blue-500', text: 'V' },
      'HBAR': { bg: 'bg-purple-800', text: 'H' },
      'ALGO': { bg: 'bg-gray-700', text: 'A' },
      'MANA': { bg: 'bg-red-400', text: 'M' },
      'SAND': { bg: 'bg-blue-200', text: 'S' },
      'AXS': { bg: 'bg-blue-600', text: 'A' }
    };
    
    return iconStyles[symbol] || { bg: 'bg-gray-500', text: symbol.charAt(0) };
  };

  const style = getIconStyle(symbol);

  return (
    <div className={`crypto-icon ${style.bg} ${className}`}>
      {style.text}
    </div>
  );
};

const MiniSparkline = ({ data, isPositive, className = "" }) => {
  // Generate mock sparkline data for demonstration
  const generateSparklineData = () => {
    const points = 20;
    const data = [];
    let value = 50;
    
    for (let i = 0; i < points; i++) {
      value += (Math.random() - 0.5) * 10;
      value = Math.max(10, Math.min(90, value));
      data.push(value);
    }
    
    return data;
  };

  const sparklineData = data || generateSparklineData();
  const maxValue = Math.max(...sparklineData);
  const minValue = Math.min(...sparklineData);
  const range = maxValue - minValue || 1;

  const pathData = sparklineData
    .map((value, index) => {
      const x = (index / (sparklineData.length - 1)) * 80;
      const y = 40 - ((value - minValue) / range) * 40;
      return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
    })
    .join(' ');

  return (
    <svg width="80" height="40" className={className}>
      <path
        d={pathData}
        className={isPositive ? 'sparkline-positive' : 'sparkline-negative'}
      />
    </svg>
  );
};

const ExchangeBadges = ({ exchanges }) => {
  const exchangeMap = {
    'binance': 'B',
    'coinbase': 'C',
    'kucoin': 'K'
  };

  return (
    <div className="flex gap-1">
      {Object.keys(exchanges).map((exchange) => (
        <span key={exchange} className="exchange-badge">
          {exchangeMap[exchange] || exchange.charAt(0).toUpperCase()}
        </span>
      ))}
    </div>
  );
};

const CryptoCard = ({ crypto }) => {
  const isPositive = crypto.change_24h_percent >= 0;
  const formattedPrice = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: crypto.price < 1 ? 4 : 2,
    maximumFractionDigits: crypto.price < 1 ? 6 : 2,
  }).format(crypto.price);

  const formattedChange = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    signDisplay: 'always',
    minimumFractionDigits: 2,
    maximumFractionDigits: 4,
  }).format(crypto.change_24h);

  const formattedPercent = new Intl.NumberFormat('en-US', {
    style: 'percent',
    signDisplay: 'always',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(crypto.change_24h_percent / 100);

  return (
    <div className="crypto-card group">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <CryptoIcon symbol={crypto.symbol} />
          <div>
            <h3 className="font-semibold text-lg">{crypto.symbol}</h3>
            <p className="text-sm text-muted-foreground">{crypto.name}</p>
          </div>
        </div>
        <ExchangeBadges exchanges={crypto.exchanges} />
      </div>

      <div className="flex items-end justify-between">
        <div className="flex-1">
          <div className="text-2xl font-bold mb-1">{formattedPrice}</div>
          <div className="flex items-center gap-2">
            <div className={`flex items-center gap-1 text-sm font-medium ${
              isPositive ? 'text-crypto-green' : 'text-crypto-red'
            }`}>
              {isPositive ? (
                <TrendingUp className="w-4 h-4" />
              ) : (
                <TrendingDown className="w-4 h-4" />
              )}
              {formattedPercent}
            </div>
            <div className={`text-xs ${
              isPositive ? 'text-crypto-green' : 'text-crypto-red'
            }`}>
              {formattedChange}
            </div>
          </div>
          <div className="text-xs text-muted-foreground mt-1">
            {crypto.price_sources} source{crypto.price_sources !== 1 ? 's' : ''}
          </div>
        </div>
        
        <div className="ml-4">
          <MiniSparkline isPositive={isPositive} />
        </div>
      </div>
    </div>
  );
};

export default CryptoCard;

