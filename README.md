# Proyecto Stream de datos de Binance: trades en tiempo real para criptomonedas

![Texto alternativo](https://bs-uploads.toptal.io/blackfish-uploads/components/blog_post_page/4087184/cover_image/regular_1708x683/Untitled-c7f4c86ddb44556b00a31a37e4219c3d.png)

## Enlaces a la API y documentación del stream

El stream de datos seleccionado proviene de **Binance**, una de las plataformas de intercambio de criptomonedas más grandes del mundo. Binance ofrece acceso en tiempo real a datos de mercado mediante APIs REST y WebSockets, permitiendo recibir información instantánea sobre operaciones, precios y profundidad de mercado.

El enlace a la documentación oficial es el siguiente:

### WebSocket (Streaming en tiempo real)

- Documentación general: <https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams>
- Base endpoint WebSocket: `wss://stream.binance.com:9443/ws`
- Streams combinados: `wss://stream.binance.com:9443/stream`
- Trade Streams: <https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams#trade-streams>
- Aggregate Trade Streams: <https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams#aggregate-trade-streams>
- Kline/Candlestick Streams: <https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams#klinecandlestick-streams>

### REST API

- Documentación REST Spot API: <https://developers.binance.com/docs/binance-spot-api-docs/rest-api>
- Exchange Info: <https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints#exchange-information>
- Order Book: <https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#order-book>
- Recent Trades: <https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#recent-trades-list>

---

## Resumen

El proyecto utiliza un stream en tiempo real mediante WebSocket para recibir operaciones ejecutadas de criptomonedas contra USDT. En este caso se monitorean simultáneamente los siguientes pares:

- BTCUSDT (Bitcoin)
- ETHUSDT (Ethereum)
- SOLUSDT (Solana)
- XRPUSDT (Ripple)

Cada evento recibido representa una operación ejecutada en el mercado spot de Binance e incluye precio, cantidad, tiempo y dirección del trade.

---

## Código utilizado

```python
import websocket
import ssl
import json

url = (
    "wss://stream.binance.com:9443/stream?"
    "streams="
    "btcusdt@trade/"
    "ethusdt@trade/"
    "solusdt@trade/"
    "xrpusdt@trade"
)

def on_open(ws):
    print("Conectado")

def on_message(ws, msg):
    data = json.loads(msg)
    print(data)

def on_error(ws, error):
    print("ERROR:", error)

def on_close(ws, code, msg):
    print("Cerrado")

ws = websocket.WebSocketApp(
    url,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever(
    sslopt={"cert_reqs": ssl.CERT_NONE}
)
```

## Origen y Autoría

Los datos del stream son recolectados y distribuidos por **Binance**, una de las plataformas de intercambio de criptomonedas más grandes del mundo y uno de los principales proveedores de liquidez en mercados spot y derivados. Binance obtiene la información directamente de las órdenes y operaciones ejecutadas dentro de su propio ecosistema de trading, y posteriormente la distribuye en tiempo real mediante sus APIs REST y WebSocket.

En este proyecto se consumen datos directamente desde la infraestructura oficial de Binance mediante el endpoint WebSocket:

`wss://stream.binance.com:9443/stream`

La conexión utilizada recibe operaciones en tiempo real de múltiples activos simultáneamente mediante **streams combinados**, específicamente:

- BTCUSDT (Bitcoin / Tether)
- ETHUSDT (Ethereum / Tether)
- SOLUSDT (Solana / Tether)
- XRPUSDT (XRP / Tether)

Cada mensaje recibido representa una transacción ejecutada dentro del mercado spot de Binance, reflejando precio, cantidad operada, tiempo exacto e identificador único del trade.

Binance mantiene centros de infraestructura distribuidos globalmente para minimizar latencia y ofrecer disponibilidad internacional, permitiendo conexiones simultáneas desde distintos países mediante sockets persistentes de alta frecuencia.

[Ver documentación oficial de Binance Spot API](https://developers.binance.com/docs/binance-spot-api-docs)

---

## Diccionario de datos

### Evento de Trade (`trade`) — disponible vía WebSocket en vivo

| Atributo | Tipo de dato | Descripción |
|----------|--------------|-------------|
| `stream` | string | Nombre del canal que originó el mensaje (`btcusdt@trade`, etc.). |
| `data.e` | string | Tipo de evento. Siempre `"trade"`. |
| `data.E` | integer | Timestamp del evento en Unix Milliseconds (UTC). |
| `data.s` | string | Símbolo del activo negociado (`BTCUSDT`, `ETHUSDT`, etc.). |
| `data.t` | integer | ID único del trade ejecutado. |
| `data.p` | number/string | Precio de ejecución del trade. |
| `data.q` | number/string | Cantidad negociada del activo base. |
| `data.T` | integer | Timestamp exacto del trade en Unix Milliseconds (UTC). |
| `data.m` | boolean | `true` si el comprador fue maker; `false` si fue taker. |
| `data.M` | boolean | Campo interno reservado por Binance. |

---

### Decodificación del nombre del stream

Ejemplo:

```text
btcusdt@trade
│      │
│      └── Tipo de evento recibido (trade)
└───────── Par de trading BTC contra USDT
```

## Variables Cuantitativas

Las variables cuantitativas del stream son:

- `data.p`: Precio ejecutado del activo.
- `data.q`: Cantidad negociada.
- `data.t`: Identificador numérico único del trade.
- `data.E`: Timestamp del evento en Unix Milliseconds.
- `data.T`: Timestamp real de ejecución del trade en Unix Milliseconds.

---

## Variables Cualitativas

Las variables cualitativas son:

- `stream`: Canal desde donde proviene el mensaje (`btcusdt@trade`, `ethusdt@trade`, etc.).
- `data.e`: Tipo de evento (`trade`).
- `data.s`: Símbolo del activo (`BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`).
- `data.m`: Indica si el comprador fue maker (`true`) o taker (`false`).
- `data.M`: Campo interno/reservado de Binance.

Del campo `data.s` se pueden extraer subvariables cualitativas:

- Activo base (`BTC`, `ETH`, `SOL`, `XRP`)
- Activo cotizado (`USDT`)

---

## Texto No Estructurado

El stream de datos **no cuenta con variables de texto no estructuradas**. Todos los campos son numéricos, categóricos o timestamps. Los campos `stream` y `data.s` son identificadores estructurados, no texto libre.

---

## Series Temporales

Las variables con marcas de tiempo son:

- `data.E`: Timestamp del evento.
- `data.T`: Timestamp real del trade.

Ambas variables vienen en formato **Unix Timestamp en milisegundos (UTC)**, por lo que pueden convertirse posteriormente a fecha y hora local para análisis temporal.

---

## Consideraciones éticas

El procesamiento del stream de datos de Binance no implica el manejo de datos personales, ya que la información corresponde únicamente a actividad pública del mercado de criptomonedas (precios, cantidades y tiempos de transacción). Sin embargo, existen consideraciones importantes:

- Puede utilizarse para trading algorítmico de alta frecuencia.
- Usuarios con menor latencia pueden tener ventaja competitiva.
- Los datos pueden presentar alta volatilidad y cambios bruscos.
- Deben respetarse los límites de uso y términos de servicio de Binance.
- Es importante utilizar la información de forma responsable y transparente.

---

## Ejemplos Reales de Datos

### BTCUSDT

```json
{
  "stream": "btcusdt@trade",
  "data": {
    "e": "trade",
    "s": "BTCUSDT",
    "p": "75901.14000000",
    "q": "0.00025000",
    "m": false
  }
}
```
---

## Consideraciones éticas 
El procesamiento del stream de datos de mercado proporcionado por Binance no implica el manejo de datos personales, ya que la información corresponde únicamente a actividad pública del mercado financiero (precios, volumen y tiempos de transacción). Sin embargo, existen consideraciones éticas relacionadas con el posible sesgo inherente al mercado, el uso desigual del acceso a datos en tiempo real y la necesidad de respetar los términos de uso del proveedor y las regulaciones financieras. Por ello, es importante utilizar estos datos de manera responsable y transparente en aplicaciones o análisis.


---


## Bibliografía

Binance. (2026). *Spot API Documentation*. <https://developers.binance.com/docs/binance-spot-api-docs>

Binance. (2026). *WebSocket Streams Documentation*. <https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams>

Binance. (2026). *Market Data Endpoints*. <https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints>

Binance. (2026). *General API Information*. <https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-api-information>


