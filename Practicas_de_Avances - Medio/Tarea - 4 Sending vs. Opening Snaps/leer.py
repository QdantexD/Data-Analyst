import psycopg2
import pandas as pd

# Conexión
conexion = psycopg2.connect(
    dbname="prueba_python",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)
cursor = conexion.cursor()

# Consulta
query = """
WITH activity_summary AS (
    SELECT 
        ab.age_bucket,
        SUM(CASE WHEN a.activity_type = 'send' THEN a.time_spent ELSE 0 END) AS total_send,
        SUM(CASE WHEN a.activity_type = 'open' THEN a.time_spent ELSE 0 END) AS total_open
    FROM activities a
    JOIN age_breakdown ab ON a.user_id = ab.user_id
    WHERE a.activity_type IN ('send','open')
    GROUP BY ab.age_bucket
)
SELECT 
    age_bucket,
    ROUND( (100.0 * total_send / NULLIF(total_send + total_open,0))::numeric, 2 ) AS send_perc,
    ROUND( (100.0 * total_open / NULLIF(total_send + total_open,0))::numeric, 2 ) AS open_perc
FROM activity_summary
ORDER BY age_bucket;
"""

cursor.execute(query)
resultados = cursor.fetchall()
df = pd.DataFrame(resultados, columns=["age_bucket","send_perc","open_perc"])
print(df)

cursor.close()
conexion.close()
