import psycopg2
import pandas as pd

# Conexión a PostgreSQL
conexion = psycopg2.connect(
    dbname="prueba_python",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)
cursor = conexion.cursor()

# Query
query = """
WITH ranked AS (
    SELECT 
        user_id,
        spend,
        transaction_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY transaction_date) AS rn
    FROM transactions
)
SELECT user_id, spend, transaction_date
FROM ranked
WHERE rn = 3;
"""

cursor.execute(query)
resultados = cursor.fetchall()

# Pasar a DataFrame para visualizar mejor
df = pd.DataFrame(resultados, columns=["user_id", "spend", "transaction_date"])
print(df)

cursor.close()
conexion.close()
