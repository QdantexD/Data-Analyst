import psycopg2
import pandas as pd

# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="prueba_python",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)

# Consulta SQL
query = """
SELECT 
    user_id,
    tweet_date,
    ROUND(AVG(tweet_count) 
          OVER (
              PARTITION BY user_id 
              ORDER BY tweet_date 
              ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
          )::numeric, 2) AS rolling_avg_3d
FROM tweets
ORDER BY user_id, tweet_date;
"""

# Leer resultados en DataFrame
df = pd.read_sql(query, conn)

# Exportar resultados a TXT
with open("tweets_resultados.txt", "w") as f:
    f.write(df.to_string(index=False))

print("✅ Resultados guardados en tweets_resultados.txt")

# Cerrar conexión
conn.close()
