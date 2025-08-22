import psycopg2

# Conexión a PostgreSQL
conexion = psycopg2.connect(
    dbname="prueba_python",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)

cur = conexion.cursor()

# 3️⃣ Consulta: vistas de laptops y móviles (tablet + phone)
cur.execute("""
SELECT
    SUM(CASE WHEN device_type = 'laptop' THEN 1 ELSE 0 END) AS laptop_views,
    SUM(CASE WHEN device_type IN ('tablet','phone') THEN 1 ELSE 0 END) AS mobile_views
FROM viewership;
""")

resultados = cur.fetchall()

print("Total de vistas:")
for row in resultados:
    print("Laptop Views:", row[0], "Mobile Views:", row[1])

# 4️⃣ Cerrar la conexión
cur.close()
conexion.close()