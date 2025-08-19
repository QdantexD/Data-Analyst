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

cur.execute("""
SELECT sender_id,
       COUNT(*) AS message_count
FROM messages
WHERE EXTRACT(YEAR FROM sent_date) = 2022
  AND EXTRACT(MONTH FROM sent_date) = 8
GROUP BY sender_id
ORDER BY message_count DESC
LIMIT 2;
""")

resultados = cur.fetchall()

print("Top 2 Power Users en agosto 2022:")
for row in resultados:
    print("Sender ID:", row[0], "Message Count:", row[1])

# Cerrar la conexión
cur.close()
conexion.close()