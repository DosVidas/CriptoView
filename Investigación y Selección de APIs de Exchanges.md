## Investigación y Selección de APIs de Exchanges

### Binance
*   **Documentación:** https://developers.binance.com/docs/binance-spot-api-docs/rest-api
*   **Endpoints de Datos de Mercado:**
    *   `GET /api/v3/ticker/24hr`: Retorna el cambio de precio y volumen de 24 horas para un símbolo. Incluye precio actual y cambio porcentual.
    *   `GET /api/v3/ticker/price`: Retorna el precio más reciente para un símbolo o todos los símbolos.
*   **WebSockets:** Binance ofrece streams de WebSocket para datos de mercado en tiempo real, incluyendo `!ticker@arr` para todos los tickers de 24 horas o ` <symbol>@ticker` para un símbolo específico.
*   **Autenticación:** Algunos endpoints de datos de mercado son públicos y no requieren autenticación. Otros (como los de trading o cuenta) requieren API Key y Secret Key con firma HMAC SHA256.
*   **Límites de Tasa:** Varían según el endpoint. Los endpoints públicos tienen límites generosos. Es crucial revisar la documentación para los límites específicos y manejar los errores de límite de tasa.
*   **Formato de Datos:** JSON.

### Coinbase Pro (ahora Coinbase Exchange)
*   **Documentación:** https://docs.cdp.coinbase.com/exchange/docs/welcome
*   **Endpoints de Datos de Mercado:**
    *   `GET /products/<product-id>/ticker`: Obtiene información del ticker para un producto. Incluye el último precio de intercambio, tamaño, precio de compra, precio de venta y volumen de 24 horas.
    *   `GET /products/<product-id>/stats`: Obtiene estadísticas de 24 horas para un producto. Incluye volumen, precio más alto, precio más bajo, precio de apertura y precio de cierre.
*   **WebSockets:** Ofrece un feed de WebSocket para datos de mercado en tiempo real, incluyendo actualizaciones de ticker.
*   **Autenticación:** Los endpoints de datos de mercado son públicos. Los endpoints de trading requieren autenticación con API Key, Secret Key y Passphrase.
*   **Límites de Tasa:** Se aplican límites de tasa. La documentación detalla los límites específicos para cada tipo de solicitud.
*   **Formato de Datos:** JSON.

### KuCoin
*   **Documentación:** https://www.kucoin.com/docs/beginners/introduction
*   **Endpoints de Datos de Mercado:**
    *   `GET /api/v1/market/allTickers`: Obtiene los últimos tickers de todos los pares de trading. Incluye el precio actual, cambio de 24 horas, cambio porcentual de 24 horas, etc.
*   **WebSockets:** KuCoin proporciona feeds de WebSocket para datos de mercado en tiempo real, incluyendo actualizaciones de ticker.
*   **Autenticación:** Los endpoints de datos de mercado son públicos. Los endpoints de trading y cuenta requieren autenticación con API Key, Secret Key y Passphrase.
*   **Límites de Tasa:** KuCoin tiene límites de tasa para sus APIs. La documentación proporciona detalles sobre estos límites.
*   **Formato de Datos:** JSON.

### Resumen de Viabilidad Técnica para MVP
Las APIs de Binance, Coinbase Pro y KuCoin son adecuadas para el MVP. Todas ofrecen:
*   Endpoints REST para obtener precios actuales y cambios de 24 horas.
*   Funcionalidad de WebSocket para actualizaciones de precios en tiempo real, lo cual es crucial para el requisito de "tiempo real" del MVP.
*   Documentación clara sobre autenticación y límites de tasa para los endpoints de datos de mercado públicos.

Se priorizará el uso de WebSockets para las actualizaciones en tiempo real, complementado con llamadas REST para la carga inicial de datos o como fallback.

