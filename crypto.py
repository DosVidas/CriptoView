from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import asyncio
import threading
import time
from src.crypto_aggregator import crypto_aggregator

crypto_bp = Blueprint('crypto', __name__)

# Variable global para el hilo de actualización
update_thread = None
update_running = False

def start_background_updates():
    """Iniciar actualizaciones en segundo plano."""
    global update_running
    if not update_running:
        update_running = True
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(crypto_aggregator.start_periodic_update(10))

@crypto_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Endpoint de verificación de salud."""
    return jsonify({
        'status': 'healthy',
        'timestamp': int(time.time()),
        'service': 'CriptoView Backend'
    })

@crypto_bp.route('/crypto/prices', methods=['GET'])
@cross_origin()
def get_crypto_prices():
    """Obtener precios actuales de criptomonedas."""
    try:
        # Si no hay datos, hacer una agregación inicial
        if not crypto_aggregator.get_latest_data():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(crypto_aggregator.aggregate_data())
            loop.close()
        
        data = crypto_aggregator.get_latest_data()
        
        # Formatear datos para el frontend
        formatted_data = []
        for symbol, symbol_data in data.items():
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
                'name': get_crypto_name(symbol),
                'price': primary_price,
                'change_24h': primary_change_24h,
                'change_24h_percent': primary_change_24h_percent,
                'exchanges': symbol_data['exchanges'],
                'price_sources': symbol_data['price_sources'],
                'timestamp': symbol_data['timestamp']
            })
        
        # Ordenar por capitalización de mercado (aproximada por precio * volumen)
        formatted_data.sort(key=lambda x: x['price'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': formatted_data,
            'timestamp': int(time.time()),
            'total_symbols': len(formatted_data)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': int(time.time())
        }), 500

@crypto_bp.route('/crypto/start-updates', methods=['POST'])
@cross_origin()
def start_updates():
    """Iniciar actualizaciones periódicas en segundo plano."""
    global update_thread, update_running
    
    try:
        if not update_running:
            update_thread = threading.Thread(target=start_background_updates, daemon=True)
            update_thread.start()
            
            return jsonify({
                'success': True,
                'message': 'Actualizaciones periódicas iniciadas',
                'timestamp': int(time.time())
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Actualizaciones ya están en ejecución',
                'timestamp': int(time.time())
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': int(time.time())
        }), 500

def get_crypto_name(symbol: str) -> str:
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

