import psycopg2

# ---------------------------------------------------------------
# Conexión a PostgreSQL
conexion = psycopg2.connect(
    dbname="prueba_python",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)

cur = conexion.cursor()

# Consulta SQL
query = """
SELECT p.page_id
FROM pages p
LEFT JOIN page_likes pl
    ON p.page_id = pl.page_id
WHERE pl.page_id IS NULL
ORDER BY p.page_id ASC;
"""

# Ejecutar la consulta
cur.execute(query)

# Obtener resultados
resultados = cur.fetchall()

# Mostrar resultados
for row in resultados:
    print(row[0])

# Cerrar la conexión
cur.close()
conexion.close()
