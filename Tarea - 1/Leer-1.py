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
cursor = conexion.cursor()

# ---------------------------------------------------------------
# Leer todos los candidatos y sus habilidades
cursor.execute("SELECT candidate_id, skill FROM candidates;")
filas = cursor.fetchall()

print("=== Todos los candidatos y sus habilidades ===")
candidatos = {}
for fila in filas:
    candidate_id, skill = fila
    if candidate_id not in candidatos:
        candidatos[candidate_id] = []
    candidatos[candidate_id].append(skill)

# Mostrar resultados completos
for cid, skills in candidatos.items():
    print(f"Candidate ID: {cid}, Skills: {', '.join(skills)}")

# ---------------------------------------------------------------
# Filtrar candidatos que tienen Python, Tableau y PostgreSQL
cursor.execute("""
SELECT candidate_id
FROM candidates
WHERE skill IN ('Python', 'Tableau', 'PostgreSQL')
GROUP BY candidate_id
HAVING COUNT(DISTINCT skill) = 3
ORDER BY candidate_id ASC;
""")
aptos = cursor.fetchall()

print("\n=== Candidatos aptos para el puesto de Data Science ===")
for fila in aptos:
    print(f"Candidate ID: {fila[0]}")

# ---------------------------------------------------------------
# Cerrar conexión
cursor.close()
conexion.close()
