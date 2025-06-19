import asyncio
import json
import logging
import time
import sys
import os
from typing import Dict, Set
import websockets
from websockets.server import serve

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from crypto_aggregator import crypto_aggregator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketManager:
    """Gestor de conexiones WebSocket para transmisión de datos en tiempo real."""
    
    def __init__(self):
        self.connections: Set[websockets.WebSocketServerProtocol] = set()
        self.is_running = False
        
    async def register(self, websocket):
        """Registrar una nueva conexión WebSocket."""
        self.connections.add(websocket)
        logger.info(f"Nueva conexión WebSocket registrada. Total: {len(self.connections)}")
        
        # Enviar datos iniciales al cliente recién conectado
        try:
            initial_data = crypto_aggregator.get_latest_data()
            if initial_data:
                await websocket.send(json.dumps({
                    'type': 'initial_data',
                    'data': self.format_data_for_frontend(initial_data),
                    'timestamp': int(time.time())
                }))
        except Exception as e:
            logger.error(f"Error enviando datos iniciales: {e}")
    
    async def unregister(self, websocket):
        """Desregistrar una conexión WebSocket."""
        self.connections.discard(websocket)
        logger.info(f"Conexión WebSocket desregistrada. Total: {len(self.connections)}")
    
    async def broadcast(self, message: dict):
        """Enviar un mensaje a todas las conexiones activas."""
        if not self.connections:
            return
        
        message_str = json.dumps(message)
        disconnected = set()
        
        for websocket in self.connections.copy():
            try:
                await websocket.send(message_str)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(websocket)
            except Exception as e:
                logger.error(f"Error enviando mensaje a WebSocket: {e}")
                disconnected.add(websocket)
        
        # Limpiar conexiones desconectadas
        for websocket in disconnected:
            self.connections.discard(websocket)
        
        if disconnected:
            logger.info(f"Limpiadas {len(disconnected)} conexiones desconectadas")
    
    def format_data_for_frontend(self, crypto_data: Dict) -> list:
        """Formatear datos de criptomonedas para el frontend."""
        formatted_data = []
        
        for symbol, symbol_data in crypto_data.items():
            # Usar el precio de Binance como principal, o el promedio si no está disponible
            primary_price = symbol_data['average_price']
            primary_change_24h = 0
            primary_change_24h_percent = 0
            
            # Priorizar Binance para datos principales
            if 'binance' in symbol_data['exchanges']:
                binance_data = symbol_data['exchanges']['binance']
                primary_price = binance_data['price']
                primary_change_24h = binance_data['change_24h']
                primary_change_24h_percent = binance_data['change_24h_percent']
            elif 'kucoin' in symbol_data['exchanges']:
                kucoin_data = symbol_data['exchanges']['kucoin']
                primary_price = kucoin_data['price']
                primary_change_24h = kucoin_data['change_24h']
                primary_change_24h_percent = kucoin_data['change_24h_percent']
            elif 'coinbase' in symbol_data['exchanges']:
                coinbase_data = symbol_data['exchanges']['coinbase']
                primary_price = coinbase_data['price']
                primary_change_24h = coinbase_data['change_24h']
                primary_change_24h_percent = coinbase_data['change_24h_percent']
            
            formatted_data.append({
                'symbol': symbol,
                'name': self.get_crypto_name(symbol),
                'price': primary_price,
                'change_24h': primary_change_24h,
                'change_24h_percent': primary_change_24h_percent,
                'exchanges': symbol_data['exchanges'],
                'price_sources': symbol_data['price_sources'],
                'timestamp': symbol_data['timestamp']
            })
        
        # Ordenar por precio (aproximación de capitalización de mercado)
        formatted_data.sort(key=lambda x: x['price'], reverse=True)
        return formatted_data
    
    def get_crypto_name(self, symbol: str) -> str:
        """Obtener el nombre completo de la criptomoneda."""
        names = {
            'BTC': 'Bitcoin',
            'ETH': 'Ethereum',
            'BNB': 'BNB',
            'XRP': 'XRP',
            'ADA': 'Cardano',
            'SOL': 'Solana',
            'DOGE': 'Dogecoin',
            'DOT': 'Polkadot',
            'MATIC': 'Polygon',
            'LTC': 'Litecoin',
            'SHIB': 'Shiba Inu',
            'TRX': 'TRON',
            'AVAX': 'Avalanche',
            'UNI': 'Uniswap',
            'ATOM': 'Cosmos',
            'LINK': 'Chainlink',
            'XMR': 'Monero',
            'ETC': 'Ethereum Classic',
            'BCH': 'Bitcoin Cash',
            'NEAR': 'NEAR Protocol',
            'APT': 'Aptos',
            'QNT': 'Quant',
            'ICP': 'Internet Computer',
            'FIL': 'Filecoin',
            'VET': 'VeChain',
            'HBAR': 'Hedera',
            'ALGO': 'Algorand',
            'MANA': 'Decentraland',
            'SAND': 'The Sandbox',
            'AXS': 'Axie Infinity'
        }
        return names.get(symbol, symbol)
    
    async def start_data_streaming(self):
        """Iniciar el streaming de datos en tiempo real."""
        self.is_running = True
        logger.info("Iniciando streaming de datos WebSocket...")
        
        while self.is_running:
            try:
                # Obtener datos actualizados
                await crypto_aggregator.aggregate_data()
                latest_data = crypto_aggregator.get_latest_data()
                
                if latest_data and self.connections:
                    # Formatear y enviar datos a todos los clientes
                    formatted_data = self.format_data_for_frontend(latest_data)
                    message = {
                        'type': 'price_update',
                        'data': formatted_data,
                        'timestamp': int(time.time())
                    }
                    
                    await self.broadcast(message)
                    logger.info(f"Datos enviados a {len(self.connections)} conexiones")
                
                # Esperar 10 segundos antes de la siguiente actualización
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Error en streaming de datos: {e}")
                await asyncio.sleep(5)  # Esperar menos tiempo en caso de error
    
    def stop_streaming(self):
        """Detener el streaming de datos."""
        self.is_running = False
        logger.info("Streaming de datos detenido")

# Instancia global del gestor WebSocket
ws_manager = WebSocketManager()

async def websocket_handler(websocket, path):
    """Manejador principal de conexiones WebSocket."""
    await ws_manager.register(websocket)
    
    try:
        # Mantener la conexión activa y manejar mensajes del cliente
        async for message in websocket:
            try:
                data = json.loads(message)
                
                # Manejar diferentes tipos de mensajes del cliente
                if data.get('type') == 'ping':
                    await websocket.send(json.dumps({
                        'type': 'pong',
                        'timestamp': int(time.time())
                    }))
                elif data.get('type') == 'request_data':
                    # Cliente solicita datos actuales
                    current_data = crypto_aggregator.get_latest_data()
                    if current_data:
                        await websocket.send(json.dumps({
                            'type': 'data_response',
                            'data': ws_manager.format_data_for_frontend(current_data),
                            'timestamp': int(time.time())
                        }))
                        
            except json.JSONDecodeError:
                logger.warning("Mensaje WebSocket inválido recibido")
            except Exception as e:
                logger.error(f"Error procesando mensaje WebSocket: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info("Conexión WebSocket cerrada por el cliente")
    except Exception as e:
        logger.error(f"Error en conexión WebSocket: {e}")
    finally:
        await ws_manager.unregister(websocket)

async def start_websocket_server(host='0.0.0.0', port=8765):
    """Iniciar el servidor WebSocket."""
    logger.info(f"Iniciando servidor WebSocket en {host}:{port}")
    
    # Inicializar el agregador de datos
    await crypto_aggregator.init_session()
    
    # Iniciar el servidor WebSocket
    server = await serve(websocket_handler, host, port)
    
    # Iniciar el streaming de datos en segundo plano
    streaming_task = asyncio.create_task(ws_manager.start_data_streaming())
    
    logger.info("Servidor WebSocket iniciado exitosamente")
    
    try:
        # Mantener el servidor ejecutándose
        await server.wait_closed()
    except KeyboardInterrupt:
        logger.info("Deteniendo servidor WebSocket...")
    finally:
        ws_manager.stop_streaming()
        streaming_task.cancel()
        await crypto_aggregator.close_session()
        server.close()
        await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_websocket_server())

