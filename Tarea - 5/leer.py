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

# Consulta: días entre primer y último post de 2021 para usuarios con >=2 posts
cur.execute("""
SELECT user_id,
       DATE_PART('day', MAX(post_date) - MIN(post_date)) AS days_between
FROM posts
WHERE EXTRACT(YEAR FROM post_date) = 2021
GROUP BY user_id
HAVING COUNT(*) >= 2
ORDER BY user_id;
""")

resultados = cur.fetchall()

print("Días entre primer y último post en 2021 para usuarios con al menos 2 posts:")
for row in resultados:
    print("User ID:", row[0], "Days Between:", int(row[1]))

# 4️⃣ Cerrar la conexión
cur.close()
conexion.close()
