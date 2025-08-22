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

# Ejecutar consulta
query = """
SELECT u.city, COUNT(t.order_id) AS total_orders
FROM trades t
JOIN users u ON t.user_id = u.user_id
WHERE t.status = 'Completed'
GROUP BY u.city
ORDER BY total_orders DESC
LIMIT 3;
"""
cursor.execute(query)

# Obtener resultados
resultados = cursor.fetchall()

# Mostrar en DataFrame (más bonito)
df = pd.DataFrame(resultados, columns=["city", "total_orders"])
print(df)

# Cerrar conexión
cursor.close()
conexion.close()
