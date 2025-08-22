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

# 1️⃣ Crear tabla viewership
cur.execute("""
DROP TABLE IF EXISTS viewership;

CREATE TABLE viewership (
    user_id INTEGER,
    device_type VARCHAR(50),
    view_time TIMESTAMP
);
""")

# 2️⃣ Insertar datos de ejemplo
cur.execute("""
INSERT INTO viewership (user_id, device_type, view_time) VALUES
(123, 'tablet', '2022-01-02 00:00:00'),
(125, 'laptop', '2022-01-07 00:00:00'),
(128, 'laptop', '2022-02-09 00:00:00'),
(129, 'phone', '2022-02-09 00:00:00'),
(145, 'tablet', '2022-02-24 00:00:00');
""")

conexion.commit()  # Guardar cambios

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
