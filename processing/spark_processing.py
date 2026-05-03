from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
import csv

# =========================================================
# 📁 RUTA LOCAL DESCARGAS (cualquier computadora)
# =========================================================
downloads = Path.home() / "Downloads"
downloads.mkdir(exist_ok=True)

# =========================================================
# 🚀 SPARK SESSION (CLUSTER REMOTO)
# =========================================================
spark = SparkSession.builder \
    .appName("CryptoProcessing") \
    .master("spark://spark-master:6077") \
    .config(
        "spark.jars.packages",
        "com.datastax.spark:spark-cassandra-connector_2.12:3.5.1"
    ) \
    .config("spark.cassandra.connection.host", "10.15.20.35") \
    .config("spark.cassandra.auth.username", "cassandra") \
    .config("spark.cassandra.auth.password", "cassandra") \
    .getOrCreate()

print("✅ Spark conectado")
print("✅ Master:", spark.sparkContext.master)
print("✅ App ID:", spark.sparkContext.applicationId)

# =========================================================
# 📥 LEER DATOS DE CASSANDRA
# =========================================================
df = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="crypto_trades", keyspace="crypto") \
    .load()

print(f"📊 COUNT: {df.count()}")
df.printSchema()

# =========================================================
# 🔧 FUNCIÓN AUXILIAR PARA EXPORTAR CSV
# =========================================================
def export_csv(dataframe, file_path, headers):
    rows = dataframe.collect()

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for row in rows:
            writer.writerow([row[h] for h in headers])

    print(f"✅ Archivo creado: {file_path}")

# =========================================================
# 📈 AVG PRICE
# =========================================================
avg_df = df.groupBy("symbol").agg(
    F.avg("price").alias("avg_price")
)

export_csv(
    avg_df,
    downloads / "avg_price.csv",
    ["symbol", "avg_price"]
)

# =========================================================
# 📊 TOTAL VOLUME
# =========================================================
volume_df = df.groupBy("symbol").agg(
    F.sum("quantity").alias("total_volume")
)

export_csv(
    volume_df,
    downloads / "volume.csv",
    ["symbol", "total_volume"]
)

# =========================================================
# ⏱️ TRADES POR MINUTO
# =========================================================
trades_window = df.groupBy(
    "symbol",
    F.window("trade_time", "1 minute")
).count()

trades_fixed = trades_window.select(
    "symbol",
    F.col("window.start").alias("window_start"),
    F.col("window.end").alias("window_end"),
    "count"
)

export_csv(
    trades_fixed,
    downloads / "trades_per_min.csv",
    ["symbol", "window_start", "window_end", "count"]
)

# =========================================================
# 💰 PRECIO MÁXIMO Y MÍNIMO
# =========================================================
price_stats = df.groupBy("symbol").agg(
    F.max("price").alias("max_price"),
    F.min("price").alias("min_price")
)

export_csv(
    price_stats,
    downloads / "price_stats.csv",
    ["symbol", "max_price", "min_price"]
)

# =========================================================
# 📉 VOLATILIDAD (DESVIACIÓN ESTÁNDAR)
# =========================================================
volatility_df = df.groupBy("symbol").agg(
    F.stddev("price").alias("price_stddev")
)

export_csv(
    volatility_df,
    downloads / "volatility.csv",
    ["symbol", "price_stddev"]
)

# =========================================================
# 📦 TRADE PROMEDIO
# =========================================================
avg_trade_size = df.groupBy("symbol").agg(
    F.avg("quantity").alias("avg_trade_quantity")
)

export_csv(
    avg_trade_size,
    downloads / "avg_trade_size.csv",
    ["symbol", "avg_trade_quantity"]
)

# =========================================================
# 🟢 BUY VS 🔴 SELL
# =========================================================
side_df = df.groupBy("symbol", "is_buyer_maker").count()

export_csv(
    side_df,
    downloads / "buy_sell_distribution.csv",
    ["symbol", "is_buyer_maker", "count"]
)

# =========================================================
# 💵 VALOR TOTAL NEGOCIADO
# =========================================================
notional_df = df.withColumn(
    "trade_value",
    F.col("price") * F.col("quantity")
).groupBy("symbol").agg(
    F.sum("trade_value").alias("total_traded_value")
)

export_csv(
    notional_df,
    downloads / "notional_value.csv",
    ["symbol", "total_traded_value"]
)

# =========================================================
# 🥇 TOP MONEDAS POR ACTIVIDAD
# =========================================================
top_symbols = df.groupBy("symbol").count() \
    .orderBy(F.desc("count"))

export_csv(
    top_symbols,
    downloads / "top_symbols.csv",
    ["symbol", "count"]
)

# =========================================================
# 🔥 FINALIZAR
# =========================================================
print("🔥 Procesamiento terminado")
spark.stop()