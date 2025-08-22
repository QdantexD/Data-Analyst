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

# 1️⃣ Crear la tabla (si existe, la elimina primero)
cur.execute("""
DROP TABLE IF EXISTS parts_assembly;

CREATE TABLE parts_assembly (
    part VARCHAR(255),
    finish_date TIMESTAMP,
    assembly_step INTEGER
);
""")

# 2️⃣ Insertar datos de ejemplo
cur.execute("""
INSERT INTO parts_assembly (part, finish_date, assembly_step) VALUES
('battery', '2022-01-22 00:00:00', 1),
('battery', '2022-02-22 00:00:00', 2),
('battery', '2022-03-22 00:00:00', 3),
('bumper', '2022-01-22 00:00:00', 1),
('bumper', '2022-02-22 00:00:00', 2),
('bumper', NULL, 3),
('bumper', NULL, 4);
""")

conexion.commit()  # Guardar cambios

# 3️⃣ Consultar partes que han comenzado pero no están terminadas
cur.execute("""
SELECT part, assembly_step
FROM parts_assembly
WHERE finish_date IS NULL
ORDER BY part, assembly_step;
""")

resultados = cur.fetchall()

print("Partes no terminadas:")
for row in resultados:
    print(row[0], row[1])

# 4️⃣ Cerrar la conexión
cur.close()
conexion.close()
