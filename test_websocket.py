#!/usr/bin/env python3
"""
Script de prueba para verificar la conectividad WebSocket de CriptoView
"""

import asyncio
import json
import websockets
import time

async def test_websocket_connection():
    """Probar la conexión WebSocket y recibir datos."""
    uri = "ws://localhost:8765"
    
    try:
        print(f"Conectando a {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ Conexión WebSocket establecida exitosamente")
            
            # Enviar ping
            ping_message = {"type": "ping"}
            await websocket.send(json.dumps(ping_message))
            print("📤 Ping enviado")
            
            # Solicitar datos
            request_message = {"type": "request_data"}
            await websocket.send(json.dumps(request_message))
            print("📤 Solicitud de datos enviada")
            
            # Escuchar mensajes por 30 segundos
            timeout = 30
            start_time = time.time()
            message_count = 0
            
            print(f"🔄 Escuchando mensajes por {timeout} segundos...")
            
            while time.time() - start_time < timeout:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(message)
                    message_count += 1
                    
                    print(f"\n📨 Mensaje {message_count} recibido:")
                    print(f"   Tipo: {data.get('type', 'unknown')}")
                    
                    if data.get('type') == 'pong':
                        print("   ✅ Pong recibido - conexión activa")
                    
                    elif data.get('type') in ['initial_data', 'data_response', 'price_update']:
                        crypto_data = data.get('data', [])
                        print(f"   📊 Datos de {len(crypto_data)} criptomonedas recibidos")
                        
                        if crypto_data:
                            # Mostrar algunos ejemplos
                            for i, crypto in enumerate(crypto_data[:3]):
                                symbol = crypto.get('symbol', 'N/A')
                                price = crypto.get('price', 0)
                                change = crypto.get('change_24h_percent', 0)
                                sources = crypto.get('price_sources', 0)
                                
                                print(f"      {symbol}: ${price:.4f} ({change:+.2f}%) [{sources} fuentes]")
                            
                            if len(crypto_data) > 3:
                                print(f"      ... y {len(crypto_data) - 3} más")
                    
                    print(f"   🕒 Timestamp: {time.strftime('%H:%M:%S', time.localtime(data.get('timestamp', time.time())))}")
                    
                except asyncio.TimeoutError:
                    print("⏰ Timeout esperando mensaje (normal)")
                    continue
                except Exception as e:
                    print(f"❌ Error procesando mensaje: {e}")
                    continue
            
            print(f"\n✅ Prueba completada. Total de mensajes recibidos: {message_count}")
            
    except ConnectionRefusedError:
        print("❌ Error: No se pudo conectar al servidor WebSocket")
        print("   Verifica que el servidor esté ejecutándose en ws://localhost:8765")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    return True

async def main():
    """Función principal de prueba."""
    print("🚀 Iniciando pruebas de integración WebSocket para CriptoView")
    print("=" * 60)
    
    success = await test_websocket_connection()
    
    print("=" * 60)
    if success:
        print("✅ Todas las pruebas WebSocket pasaron exitosamente")
        print("🎉 El sistema de tiempo real está funcionando correctamente")
    else:
        print("❌ Algunas pruebas fallaron")
        print("🔧 Revisa la configuración del servidor WebSocket")
    
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)

