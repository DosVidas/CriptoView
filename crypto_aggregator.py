import asyncio
import json
import logging
import time
from typing import Dict, List, Optional
import aiohttp
import requests
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoDataAggregator:
    """Agregador de datos de criptomonedas desde múltiples exchanges."""
    
    def __init__(self):
        self.exchanges = {
            'binance': {
                'name': 'Binance',
                'base_url': 'https://api.binance.com',
                'ticker_endpoint': '/api/v3/ticker/24hr',
                'websocket_url': 'wss://stream.binance.com:9443/ws/!ticker@arr'
            },
            'coinbase': {
                'name': 'Coinbase',
                'base_url': 'https://api.exchange.coinbase.com',
                'ticker_endpoint': '/products/{symbol}/ticker',
                'stats_endpoint': '/products/{symbol}/stats'
            },
            'kucoin': {
                'name': 'KuCoin',
                'base_url': 'https://api.kucoin.com',
                'ticker_endpoint': '/api/v1/market/allTickers'
            }
        }
        
        # Lista de las principales criptomonedas por capitalización de mercado
        self.target_symbols = [
            'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT', 'MATIC', 'LTC',
            'SHIB', 'TRX', 'AVAX', 'UNI', 'ATOM', 'LINK', 'XMR', 'ETC', 'BCH', 'NEAR',
            'APT', 'QNT', 'ICP', 'FIL', 'VET', 'HBAR', 'ALGO', 'MANA', 'SAND', 'AXS'
        ]
        
        self.latest_data = {}
        self.session = None
    
    async def init_session(self):
        """Inicializar sesión HTTP asíncrona."""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        """Cerrar sesión HTTP asíncrona."""
        if self.session:
            await self.session.close()
    
    def normalize_symbol(self, symbol: str, exchange: str) -> str:
        """Normalizar símbolos de criptomonedas según el exchange."""
        if exchange == 'binance':
            return f"{symbol}USDT"
        elif exchange == 'coinbase':
            return f"{symbol}-USD"
        elif exchange == 'kucoin':
            return f"{symbol}-USDT"
        return symbol
    
    async def fetch_binance_data(self) -> Dict:
        """Obtener datos de Binance."""
        try:
            await self.init_session()
            url = f"{self.exchanges['binance']['base_url']}{self.exchanges['binance']['ticker_endpoint']}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    normalized_data = {}
                    
                    for item in data:
                        symbol = item['symbol']
                        # Filtrar solo los símbolos que nos interesan (terminados en USDT)
                        if symbol.endswith('USDT'):
                            base_symbol = symbol.replace('USDT', '')
                            if base_symbol in self.target_symbols:
                                normalized_data[base_symbol] = {
                                    'exchange': 'binance',
                                    'symbol': base_symbol,
                                    'price': float(item['lastPrice']),
                                    'change_24h': float(item['priceChange']),
                                    'change_24h_percent': float(item['priceChangePercent']),
                                    'volume_24h': float(item['volume']),
                                    'timestamp': int(time.time())
                                }
                    
                    logger.info(f"Binance: Obtenidos datos de {len(normalized_data)} símbolos")
                    return normalized_data
                else:
                    logger.error(f"Error al obtener datos de Binance: {response.status}")
                    return {}
        except Exception as e:
            logger.error(f"Error al conectar con Binance: {e}")
            return {}
    
    async def fetch_coinbase_data(self) -> Dict:
        """Obtener datos de Coinbase."""
        try:
            await self.init_session()
            normalized_data = {}
            
            # Coinbase requiere llamadas individuales por símbolo
            for symbol in self.target_symbols[:10]:  # Limitamos a 10 para el MVP
                coinbase_symbol = self.normalize_symbol(symbol, 'coinbase')
                ticker_url = f"{self.exchanges['coinbase']['base_url']}/products/{coinbase_symbol}/ticker"
                stats_url = f"{self.exchanges['coinbase']['base_url']}/products/{coinbase_symbol}/stats"
                
                try:
                    async with self.session.get(ticker_url) as ticker_response:
                        if ticker_response.status == 200:
                            ticker_data = await ticker_response.json()
                            
                            async with self.session.get(stats_url) as stats_response:
                                if stats_response.status == 200:
                                    stats_data = await stats_response.json()
                                    
                                    current_price = float(ticker_data.get('price', 0))
                                    open_price = float(stats_data.get('open', current_price))
                                    change_24h = current_price - open_price
                                    change_24h_percent = (change_24h / open_price * 100) if open_price > 0 else 0
                                    
                                    normalized_data[symbol] = {
                                        'exchange': 'coinbase',
                                        'symbol': symbol,
                                        'price': current_price,
                                        'change_24h': change_24h,
                                        'change_24h_percent': change_24h_percent,
                                        'volume_24h': float(stats_data.get('volume', 0)),
                                        'timestamp': int(time.time())
                                    }
                except Exception as e:
                    logger.warning(f"Error al obtener datos de {symbol} en Coinbase: {e}")
                    continue
            
            logger.info(f"Coinbase: Obtenidos datos de {len(normalized_data)} símbolos")
            return normalized_data
        except Exception as e:
            logger.error(f"Error al conectar con Coinbase: {e}")
            return {}
    
    async def fetch_kucoin_data(self) -> Dict:
        """Obtener datos de KuCoin."""
        try:
            await self.init_session()
            url = f"{self.exchanges['kucoin']['base_url']}{self.exchanges['kucoin']['ticker_endpoint']}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    normalized_data = {}
                    
                    if 'data' in data and 'ticker' in data['data']:
                        for item in data['data']['ticker']:
                            symbol_pair = item['symbol']
                            # Filtrar solo los símbolos que nos interesan (terminados en -USDT)
                            if symbol_pair.endswith('-USDT'):
                                base_symbol = symbol_pair.replace('-USDT', '')
                                if base_symbol in self.target_symbols:
                                    normalized_data[base_symbol] = {
                                        'exchange': 'kucoin',
                                        'symbol': base_symbol,
                                        'price': float(item['last']),
                                        'change_24h': float(item['changePrice']),
                                        'change_24h_percent': float(item['changeRate']) * 100,
                                        'volume_24h': float(item['vol']),
                                        'timestamp': int(time.time())
                                    }
                    
                    logger.info(f"KuCoin: Obtenidos datos de {len(normalized_data)} símbolos")
                    return normalized_data
                else:
                    logger.error(f"Error al obtener datos de KuCoin: {response.status}")
                    return {}
        except Exception as e:
            logger.error(f"Error al conectar con KuCoin: {e}")
            return {}
    
    async def aggregate_data(self) -> Dict:
        """Agregar datos de todos los exchanges."""
        logger.info("Iniciando agregación de datos...")
        
        # Ejecutar todas las llamadas a APIs en paralelo
        binance_task = self.fetch_binance_data()
        coinbase_task = self.fetch_coinbase_data()
        kucoin_task = self.fetch_kucoin_data()
        
        binance_data, coinbase_data, kucoin_data = await asyncio.gather(
            binance_task, coinbase_task, kucoin_task, return_exceptions=True
        )
        
        # Manejar excepciones
        if isinstance(binance_data, Exception):
            logger.error(f"Error en Binance: {binance_data}")
            binance_data = {}
        if isinstance(coinbase_data, Exception):
            logger.error(f"Error en Coinbase: {coinbase_data}")
            coinbase_data = {}
        if isinstance(kucoin_data, Exception):
            logger.error(f"Error en KuCoin: {kucoin_data}")
            kucoin_data = {}
        
        # Combinar datos de todos los exchanges
        aggregated_data = {}
        
        for symbol in self.target_symbols:
            symbol_data = {
                'symbol': symbol,
                'exchanges': {},
                'average_price': 0,
                'price_sources': 0,
                'timestamp': int(time.time())
            }
            
            total_price = 0
            price_count = 0
            
            # Agregar datos de Binance
            if symbol in binance_data:
                symbol_data['exchanges']['binance'] = binance_data[symbol]
                total_price += binance_data[symbol]['price']
                price_count += 1
            
            # Agregar datos de Coinbase
            if symbol in coinbase_data:
                symbol_data['exchanges']['coinbase'] = coinbase_data[symbol]
                total_price += coinbase_data[symbol]['price']
                price_count += 1
            
            # Agregar datos de KuCoin
            if symbol in kucoin_data:
                symbol_data['exchanges']['kucoin'] = kucoin_data[symbol]
                total_price += kucoin_data[symbol]['price']
                price_count += 1
            
            # Calcular precio promedio si hay datos disponibles
            if price_count > 0:
                symbol_data['average_price'] = total_price / price_count
                symbol_data['price_sources'] = price_count
                aggregated_data[symbol] = symbol_data
        
        self.latest_data = aggregated_data
        logger.info(f"Agregación completada: {len(aggregated_data)} símbolos procesados")
        return aggregated_data
    
    def get_latest_data(self) -> Dict:
        """Obtener los últimos datos agregados."""
        return self.latest_data
    
    async def start_periodic_update(self, interval: int = 10):
        """Iniciar actualizaciones periódicas de datos."""
        logger.info(f"Iniciando actualizaciones periódicas cada {interval} segundos")
        
        while True:
            try:
                await self.aggregate_data()
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Error en actualización periódica: {e}")
                await asyncio.sleep(interval)

# Instancia global del agregador
crypto_aggregator = CryptoDataAggregator()

