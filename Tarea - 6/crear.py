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

# 1️⃣ Crear tabla messages
cur.execute("""
DROP TABLE IF EXISTS messages;

CREATE TABLE messages (
    message_id INTEGER,
    sender_id INTEGER,
    receiver_id INTEGER,
    content VARCHAR(255),
    sent_date TIMESTAMP
);
""")

# 2️⃣ Insertar datos de ejemplo
messages_data = [
    (901, 3601, 4500, "You up?", '2022-08-03 00:00:00'),
    (902, 4500, 3601, "Only if you're buying", '2022-08-03 00:00:00'),
    (743, 3601, 8752, "Let's take this offline", '2022-06-14 00:00:00'),
    (922, 3601, 4500, "Get on the call", '2022-08-10 00:00:00')
]

cur.executemany("""
    INSERT INTO messages (message_id, sender_id, receiver_id, content, sent_date)
    VALUES (%s, %s, %s, %s, %s);
""", messages_data)

conexion.commit()  # Guardar cambios

# 3️⃣ Consulta: top 2 usuarios con más mensajes en agosto 2022
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

# 4️⃣ Cerrar la conexión
cur.close()
conexion.close()
