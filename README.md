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

El procesamiento del stream de datos de mercado proporcionado por Binance no implica el manejo de datos personales, ya que la información corresponde únicamente a actividad pública del mercado financiero (precios, volumen y tiempos de transacción). Sin embargo, existen consideraciones éticas relacionadas con el posible sesgo inherente al mercado, el uso desigual del acceso a datos en tiempo real y la necesidad de respetar los términos de uso del proveedor y las regulaciones financieras. Por ello, es importante utilizar estos datos de manera responsable y transparente en aplicaciones o análisis.

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

# Infraestructura y Configuración

![Texto alternativo](https://miro.medium.com/0*VRAoHqBR9RCkm91p.png)


## Configuración de la Capa de Ingesta (Operativa)

Para la capa operativa se seleccionó **Apache Cassandra** como base de datos NoSQL principal.

Cassandra fue elegida debido a que está diseñada para:

- Alta disponibilidad distribuida.
- Escritura rápida a gran escala.
- Replicación automática entre nodos.
- Tolerancia a fallos sin punto único de falla.
- Escalabilidad horizontal agregando nuevos nodos.

La infraestructura implementada consta de un **cluster de 3 nodos Cassandra** desplegados en contenedores Docker:

```text
cassandra-node-1
cassandra-node-2
cassandra-node-3
````

Cada nodo participa en la replicación de datos mediante estrategia distribuida.

La tabla principal del sistema es:

```sql
crypto.crypto_trades
```

donde se almacenan operaciones en tiempo real provenientes del WebSocket oficial de Binance para los pares:

* BTCUSDT
* ETHUSDT
* SOLUSDT
* XRPUSDT

La base fue optimizada para escrituras rápidas mediante claves particionadas por símbolo y ordenamiento por tiempo.

---

## Configuración de la Capa de Procesamiento Analítico (OLAP)

Para la capa analítica se seleccionó **Apache Spark** como motor OLAP distribuido.

Spark fue elegido por su capacidad de:

* Procesamiento masivo en memoria.
* Agregaciones distribuidas.
* Lectura paralela desde Cassandra.
* Integración con PySpark.
* Escalabilidad horizontal.

La infraestructura implementada consiste en:

```text
spark-master
spark-worker-1
spark-worker-2
spark-worker-3
```

Configuración cluster:

* 1 nodo Master
* 3 nodos Worker
* Ejecución distribuida sobre Docker.

El procesamiento se realiza desde un contenedor cliente denominado:

```text
crypto_processing
```

Este contenedor ejecuta jobs PySpark que generan analíticas como:

* Precio promedio por activo.
* Volumen total negociado.
* Trades por minuto.
* Máximos y mínimos.
* Volatilidad (desviación estándar).
* Tamaño promedio de trade.
* Distribución Buy vs Sell.
* Valor total transado.
* Ranking de monedas por actividad.

Los resultados se exportan en archivos CSV.

---

## Implementación de Control de Accesos

Se configuraron controles básicos de acceso en cada capa.

### Cassandra

Autenticación habilitada mediante usuario y contraseña:

```text
usuario: cassandra
password: cassandra
```

Las conexiones se realizan únicamente por puertos específicos del cluster.

### Spark

Acceso restringido a través de red privada Docker entre contenedores:

```text
spark-cluster_spark-cluster
```

Solo contenedores autorizados pueden enviar jobs al Master.

### Docker Networking

Se utilizaron redes privadas internas para separar:

* Red Cassandra.
* Red Spark.
* Contenedores cliente.

Esto evita exposición innecesaria de servicios.

---

## Código y Documentación

El repositorio contiene:

### Scripts principales

```text
ingest.py
spark_processing.py
```

### Infraestructura

```text
Dockerfile (ingesta)
Dockerfile (processing)
requirements_ingest.txt
requirements_processing.txt
```

### Documentación

* README.md
* Diagrama de arquitectura.
* Instrucciones de despliegue.
* Evidencias de ejecución.
* Logs del sistema.

---

## Justificación de Arquitectura Basada en el Teorema CAP

El diseño prioriza:

```text
AP = Disponibilidad + Tolerancia a particiones
```

### Justificación técnica

En sistemas financieros en tiempo real, como ingestión de trades cripto, es crítico que el sistema continúe disponible incluso ante fallos parciales de red o caída de nodos.

### Cassandra

Cassandra está diseñada bajo enfoque AP:

* Mantiene disponibilidad si un nodo falla.
* Replica datos entre nodos.
* Tolera particiones de red.
* Consistencia configurable eventual.

Esto la hace ideal para ingestión continua de datos streaming.

### Spark

Spark se utiliza como capa OLAP posterior, donde el análisis puede ejecutarse sobre datos ya persistidos. La consistencia se obtiene durante las lecturas batch analíticas.

### Conclusión CAP

Se priorizó:

1. Disponibilidad
2. Tolerancia a particiones
3. Consistencia eventual controlada

Porque perder temporalmente consistencia es menos crítico que detener la captura de trades en tiempo real.

---

## Arquitectura General del Proyecto

```text
Binance WebSocket
        ↓
Contenedor crypto_ingest
        ↓
Cluster Cassandra (3 nodos)
        ↓
Contenedor crypto_processing
        ↓
Cluster Spark (1 Master + 3 Workers)
        ↓
CSV Analíticos / Reportes
```

---

## Resultado Final

Se construyó una arquitectura distribuida real basada en microservicios y contenedores, capaz de ingerir datos en streaming, almacenarlos de forma resiliente y procesarlos analíticamente a escala.

# Despliegue del Proyecto con Docker (Paso a Paso)

![Texto alternativo](https://www.daniloarancibia.es/_next/image?url=https%3A%2F%2Fwww.api.daniloarancibia.es%2Fassets%2F5769261f-18b3-418b-ab89-6308848c6243&w=3840&q=75)

Este proyecto utiliza **dos contenedores independientes**:

1. **crypto_ingest**  
   Encargado de conectarse al WebSocket de Binance e insertar datos en Cassandra.

2. **crypto_processing**  
   Encargado de leer datos desde Cassandra usando PySpark y generar archivos CSV analíticos.

---

## Estructura del Proyecto

```text
proyecto_bd_nr/
│── ingest/
│   ├── Dockerfile
│   ├── requirements_ingest.txt
│   └── ingest.py
│
└── processing/
    ├── Dockerfile
    ├── requirements_processing.txt
    └── spark_processing.py
````

---

## 1. Contenedor de Ingesta (`crypto_ingest`)

## Dockerfile

Ubicación:

```text
ingest/Dockerfile
```

Contenido:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_ingest.txt .

RUN pip install --no-cache-dir -r requirements_ingest.txt

COPY ingest.py .

CMD ["python", "ingest.py"]
```

---

## requirements_ingest.txt

```txt
cassandra-driver
websocket-client
```

---

## Construcción de la Imagen

Entrar a la carpeta:

```bash
cd ingest
```

Construir imagen:

```bash
docker build -t crypto-ingest .
```

---

## Ejecución del Contenedor

```bash
docker run -d \
--name crypto_ingest \
crypyo-ingest
```

> Nota: si la imagen fue creada con nombre correcto, usar:

```bash
docker run -d \
--name crypto_ingest \
crypto-ingest
```

---

## Ver Logs

```bash
docker logs -f crypto_ingest
```

---

## 2. Contenedor de Procesamiento (`crypto_processing`)

## Dockerfile

Ubicación:

```text
processing/Dockerfile
```

Contenido:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-jdk \
    procps \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

COPY requirements_processing.txt .

RUN pip install --no-cache-dir -r requirements_processing.txt

COPY spark_processing.py .

CMD ["python", "spark_processing.py"]
```

---

## requirements_processing.txt

```txt
pyspark==3.5.7
cassandra-driver==3.30.0
pandas
pyarrow
```

---

## Construcción de la Imagen

Entrar a la carpeta:

```bash
cd processing
```

Construir imagen:

```bash
docker build --no-cache -t crypto-processing .
```

---

## Ejecución del Contenedor

```bash
docker run -d \
--name crypto_processing \
--network spark-cluster_spark-cluster \
-v ~/Downloads:/root/Downloads \
crypto-processing
```

---

## Explicación del Comando

### `--network spark-cluster_spark-cluster`

Conecta el contenedor a la red interna donde viven:

* spark-master
* spark-worker-1
* spark-worker-2
* spark-worker-3

### `-v ~/Downloads:/root/Downloads`

Guarda los archivos CSV generados directamente en la carpeta **Downloads** del host.

---

## Ver Logs

```bash
docker logs -f crypto_processing
```

---

## 3. Verificar Contenedores Activos

```bash
docker ps
```

---

## 4. Detener Contenedores

```bash
docker stop crypto_ingest crypto_processing
```

---

## 5. Eliminar Contenedores

```bash
docker rm -f crypto_ingest crypto_processing
```

---

## 6. Reconstrucción Después de Cambios

Si se modifica cualquier script Python o Dockerfile:

## Ingesta

```bash
cd ingest
docker build -t crypto-ingest .
```

## Processing

```bash
cd processing
docker build --no-cache -t crypto-processing .
```

---

# 7. Flujo General del Sistema

```text
Binance WebSocket
        ↓
crypto_ingest
        ↓
Cluster Cassandra
        ↓
crypto_processing
        ↓
Apache Spark Cluster
        ↓
CSV Analíticos
```

---

## Resultado Esperado

Al finalizar:

* Datos almacenados en Cassandra.
* Procesamiento distribuido con Spark.
* Archivos CSV disponibles en:

```text
~/Downloads
```

# Implementación de la capa de ingesta

![Texto alternativo](https://content.nationalgeographic.com.es/medio/2021/11/06/bitcoin-es-la-criptomoneda-mas-popular-y-la-que-acumula-un-mayor-valor_30d37364_1200x630.jpg)

## Estado de Verdad Operativa

La base de datos de ingesta funciona como el **stage de verdad operativa** del sistema, ya que almacena directamente los eventos originales provenientes del stream en tiempo real.

Esto permite realizar consultas puntuales sobre el estado actual y reciente del mercado con latencia mínima.

La tabla principal utilizada es:

```sql
crypto.crypto_trades
````

con la siguiente estructura lógica:

* `trade_id`
* `symbol`
* `trade_time`
* `price`
* `quantity`
* `is_buyer_maker`
* `event_time`

Una vez finalizado el proceso de ingesta, se ejecuta una validación automática consultando los primeros 10 registros almacenados en Cassandra:

```sql
SELECT * FROM crypto.crypto_trades LIMIT 10;
```

Esto permite demostrar que los datos fueron insertados correctamente y que Cassandra contiene el estado operativo real capturado desde Binance.

---

## Garantía de Caudal

El sistema fue diseñado para soportar flujos continuos de eventos financieros en tiempo real.

Para demostrar capacidad de escritura se ejecutó una prueba de ingesta continua durante varios minutos recibiendo múltiples mensajes por segundo desde Binance.

Durante la ejecución:

* No se detectaron pérdidas de mensajes.
* Cassandra aceptó escrituras concurrentes sin degradación visible.
* La latencia de inserción se mantuvo baja.
* El sistema procesó eventos de múltiples símbolos simultáneamente.

Esto confirma que Cassandra es adecuada para cargas intensivas de escritura streaming.

---

## Resiliencia

La infraestructura fue desplegada con un **cluster de 3 nodos Cassandra**, permitiendo alta disponibilidad.

```text
cassandra-node-1
cassandra-node-2
cassandra-node-3
```

Ventajas obtenidas:

* Replicación automática de datos.
* Tolerancia ante caída de nodos individuales.
* Continuidad operativa sin interrupción del servicio.
* Recuperación automática al reincorporar nodos.

En caso de falla parcial, los nodos restantes continúan respondiendo lecturas y escrituras según la política de consistencia configurada.

Esto garantiza resiliencia operativa para la capa de ingesta.


# Implementación de la Capa de Procesamiento para Analíticos

La capa analítica del proyecto fue implementada utilizando **Apache Spark con PySpark**, conectado al cluster Cassandra donde se almacenan los datos crudos provenientes del stream de Binance.

El procesamiento se ejecuta desde el contenedor:

```text
crypto_processing
````

Este componente actúa como núcleo de transformación, limpieza y análisis de datos, permitiendo convertir eventos operativos en información estratégica.

---

## Limpieza de Datos

Se desarrollaron jobs específicos en PySpark para asegurar calidad y consistencia de la información antes del análisis.

### Procesos aplicados:

* Eliminación de registros duplicados mediante claves únicas (`trade_id` + `symbol`).
* Validación de valores nulos.
* Conversión correcta de tipos de datos:

  * `price` → double
  * `quantity` → double
  * `trade_time` → timestamp
* Normalización de nombres de símbolos.
* Verificación cronológica de timestamps.

Esto garantiza integridad en los datasets utilizados para analítica.

---

## Enriquecimiento

Se realizó enriquecimiento lógico de los datos generando nuevas variables derivadas a partir del stream original.

### Variables calculadas:

* **trade_value** = `price * quantity`
* Clasificación de operación:

  * BUY
  * SELL
* Ventanas de tiempo por minuto.
* Ranking de actividad por símbolo.
* Medidas estadísticas por activo.

Esto añade contexto financiero útil para toma de decisiones.

---

## Transformación

Se aplicó lógica de negocio orientada a facilitar agregaciones masivas y consultas complejas.

### Transformaciones principales:

* Agrupación por símbolo.
* Agregaciones temporales por minuto.
* Sumatorias de volumen.
* Promedios de precio.
* Máximos y mínimos.
* Desviación estándar (volatilidad).
* Conteo de trades.
* Distribución comprador/vendedor.

Los resultados fueron exportados en archivos CSV listos para consumo analítico.

---

## Código y Documentación

El repositorio incluye:

### Código fuente

```text
spark_processing.py
```

### Infraestructura

```text
Dockerfile
requirements_processing.txt
```

### Documentación

* README.md
* Evidencias de ejecución
* Logs Spark
* Arquitectura distribuida
* Resultados CSV
* Diagramas de flujo

---

# Análisis de Resultados

![Texto alternativo](https://media.a24.com/p/e8901159a03ed0b2f0bf63364b7ae524/adjuntos/296/imagenes/008/486/0008486016/600x0/smart/moneda-digital-ethereumpng.png)

A partir de los datos procesados se generó inteligencia de negocio mediante consultas analíticas sobre operaciones reales del mercado cripto.

---

## Consultas de Valor

Se ejecutaron múltiples consultas complejas, entre ellas:

### 1. Precio promedio por criptomoneda

Permite conocer nivel medio de cotización durante la ventana analizada.

```text
avg_price.csv
```

### 2. Volumen total negociado

Identifica qué activos tuvieron mayor movimiento de mercado.

```text
volume.csv
```

### 3. Trades por minuto

Detecta momentos de alta actividad o picos operativos.

```text
trades_per_min.csv
```

### 4. Volatilidad por activo

Calculada mediante desviación estándar del precio.

```text
volatility.csv
```

### 5. Ranking de monedas por actividad

Conteo total de operaciones por símbolo.

```text
top_symbols.csv
```

### 6. Precio máximo y mínimo

Permite medir rango operativo intradía.

```text
price_stats.csv
```

### 7. Valor total transado

Capital movilizado por activo.

```text
notional_value.csv
```

---

## Trazabilidad y Evolución del Dato

Se documentó el ciclo completo de vida del dato:

```text
Evento crudo Binance JSON
        ↓
Recepción WebSocket
        ↓
Inserción Cassandra
        ↓
Lectura Spark
        ↓
Limpieza y normalización
        ↓
Agregaciones y métricas
        ↓
CSV analíticos
        ↓
Información estratégica
```

### Ejemplo real

Un trade individual recibido como:

```json
{
  "s": "BTCUSDT",
  "p": "64250.10",
  "q": "0.52"
}
```

Se transforma posteriormente en:

* volumen total BTC
* precio promedio BTC
* volatilidad BTC
* capital negociado BTC
* actividad por minuto BTC

---

## Documentación de Hallazgos

### Hallazgos relevantes:

* BTCUSDT concentró el mayor valor negociado.
* ETHUSDT mostró alta frecuencia operativa.
* Algunos minutos presentaron picos abruptos de actividad.
* Activos con mayor volatilidad implican mayor riesgo.
* La distribución BUY/SELL refleja presión de mercado.

### Impacto de negocio

Estos resultados permiten:

* Detectar oportunidades de trading.
* Medir liquidez por activo.
* Identificar activos más dinámicos.
* Monitorear riesgo intradía.
* Construir dashboards financieros.

---

## Código y Evidencias Incluidas

El repositorio contiene:

* Código PySpark completo.
* Scripts de ingesta.
* Dockerfiles.
* CSV generados.
* Logs de ejecución.
* Capturas de resultados.
* README documentado.
* Arquitectura del sistema.

---

## Resultado Final

Se construyó un pipeline completo de analítica distribuida capaz de transformar datos crudos en tiempo real en métricas estratégicas listas para inteligencia de negocio.

# Bibliografía

Binance. (2026). *Spot API Documentation*. <https://developers.binance.com/docs/binance-spot-api-docs>

Binance. (2026). *WebSocket Streams Documentation*. <https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams>

Binance. (2026). *Market Data Endpoints*. <https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints>

Binance. (2026). *General API Information*. <https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-api-information>











