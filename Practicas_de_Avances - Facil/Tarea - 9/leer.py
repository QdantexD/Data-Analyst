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

# Ejecutar la consulta
query = """
SELECT 
    EXTRACT(MONTH FROM submit_date) AS mth,
    product_id AS product,
    ROUND(AVG(stars)::numeric, 2) AS avg_stars
FROM reviews
GROUP BY mth, product_id
ORDER BY mth, product_id;
"""
cursor.execute(query)

# Obtener resultados
resultados = cursor.fetchall()

# Convertir a DataFrame
df = pd.DataFrame(resultados, columns=["mth", "product", "avg_stars"])
print(df)

# Cerrar conexión
cursor.close()
conexion.close()
