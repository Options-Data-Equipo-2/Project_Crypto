from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory

import websocket
import ssl
import json
import time
from datetime import datetime

# ========================
# CASSANDRA CONFIG
# ========================

cassandra_user = "cassandra"
cassandra_password = "cassandra"

cluster = Cluster(
    contact_points=["10.15.20.35"],
    port=9042,
    auth_provider=PlainTextAuthProvider(
        username=cassandra_user,
        password=cassandra_password
    )
)

session = cluster.connect()
session.row_factory = dict_factory

print("✅ Connected to Cassandra")

# ========================
# KEYSPACE / TABLE
# ========================

session.execute("""
CREATE KEYSPACE IF NOT EXISTS crypto
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
""")

session.set_keyspace("crypto")

session.execute("""
CREATE TABLE IF NOT EXISTS crypto_trades(
    trade_id bigint,
    symbol text,
    trade_time timestamp,
    price double,
    quantity double,
    is_buyer_maker boolean,
    event_time timestamp,
    PRIMARY KEY (symbol, trade_time, trade_id)
) WITH CLUSTERING ORDER BY (trade_time DESC)
""")

insert_trade = session.prepare("""
INSERT INTO crypto_trades (
    trade_id, symbol, trade_time, price,
    quantity, is_buyer_maker, event_time
) VALUES (?, ?, ?, ?, ?, ?, ?)
""")

# ========================
# BINANCE STREAM
# ========================

start_time = time.time()
DURATION = 240

url = (
    "wss://stream.binance.com:9443/stream?"
    "streams=btcusdt@trade/ethusdt@trade/solusdt@trade/xrpusdt@trade"
)

def on_open(ws):
    print("🚀 WebSocket conectado")

def on_message(ws, msg):
    try:
        if time.time() - start_time > DURATION:
            print("⏹️ 1 minuto terminado")
            ws.close()
            return

        data = json.loads(msg)["data"]

        symbol = data["s"]
        price = float(data["p"])
        quantity = float(data["q"])
        trade_id = data["t"]
        is_buyer_maker = data["m"]

        trade_time = datetime.fromtimestamp(data["T"] / 1000)
        event_time = datetime.fromtimestamp(data["E"] / 1000)

        session.execute(insert_trade, (
            trade_id,
            symbol,
            trade_time,
            price,
            quantity,
            is_buyer_maker,
            event_time
        ))

        print(f"💾 Insertado {symbol} | {price}")

    except Exception as e:
        print("❌ Error:", e)

def on_error(ws, error):
    print("ERROR:", error)

def on_close(ws, code, msg):
    print("🔌 Cerrado")

ws = websocket.WebSocketApp(
    url,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

# ========================
# TEST FINAL
# ========================

rows = session.execute("SELECT * FROM crypto_trades LIMIT 10")
for r in rows:
    print(r)