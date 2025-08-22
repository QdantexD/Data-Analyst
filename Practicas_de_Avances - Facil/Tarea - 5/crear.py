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

# 1️⃣ Crear la tabla posts
cur.execute("""
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    user_id INTEGER,
    post_id INTEGER,
    post_content TEXT,
    post_date TIMESTAMP
);
""")

# 2️⃣ Insertar datos de ejemplo usando escape correcto
posts_data = [
    (151652, 599415, 'Need a hug', '2021-07-10 12:00:00'),
    (661093, 624356, "Bed. Class 8-12. Work 12-3. Gym 3-5 or 6. Then class 6-10. Another day that's gonna fly by. I miss my girlfriend", '2021-07-29 13:00:00'),
    (4239, 784254, 'Happy 4th of July!', '2021-07-04 11:00:00'),
    (661093, 442560, 'Just going to cry myself to sleep after watching Marley and Me.', '2021-07-08 14:00:00'),
    (151652, 111766, "I'm so done with covid - need travelling ASAP!", '2021-07-12 19:00:00')
]

cur.executemany("""
    INSERT INTO posts (user_id, post_id, post_content, post_date)
    VALUES (%s, %s, %s, %s);
""", posts_data)

conexion.commit()  # Guardar cambios

# 3️⃣ Consulta: días entre primer y último post de 2021 para usuarios con >=2 posts
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
