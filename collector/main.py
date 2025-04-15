print("🔧 Zox coletor iniciou! Verificando execução...")

import time
import requests
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MOEDA = 'BNBUSDT'
INTERVALO = 5

conn = psycopg2.connect(
    host="SEU_HOST",
    dbname="railway",
    user="postgres",
    password=os.environ.get("POSTGRES_PASSWORD"),
    port=5432
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bd_ia (
    id SERIAL PRIMARY KEY,
    moeda VARCHAR(20),
    preco NUMERIC,
    timestamp TIMESTAMP
)
""")
conn.commit()

print(f"🔄 Iniciando coleta de {MOEDA} a cada {INTERVALO}s...")

while True:
    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={MOEDA}")
        data = response.json()
        preco = float(data['price'])
        agora = datetime.now()

        cursor.execute("INSERT INTO bd_ia (moeda, preco, timestamp) VALUES (%s, %s, %s)",
                       (MOEDA, preco, agora))
        conn.commit()

        print(f"[{agora.strftime('%H:%M:%S')}] {MOEDA} = {preco}")
        time.sleep(INTERVALO)

    except Exception as e:
        print("❌ Erro na coleta:", e)
        time.sleep(10)
