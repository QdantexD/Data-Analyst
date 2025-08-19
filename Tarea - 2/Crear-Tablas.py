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

# 1️⃣ Crear tablas
cur.execute("""
DROP TABLE IF EXISTS page_likes;
DROP TABLE IF EXISTS pages;

CREATE TABLE pages (
    page_id INTEGER PRIMARY KEY,
    page_name VARCHAR(255)
);

CREATE TABLE page_likes (
    user_id INTEGER,
    page_id INTEGER,
    liked_date TIMESTAMP,
    FOREIGN KEY (page_id) REFERENCES pages(page_id)
);
""")

# 2️⃣ Insertar datos de prueba
cur.execute("""
INSERT INTO pages (page_id, page_name) VALUES
(20001, 'SQL Solutions'),
(20045, 'Brain Exercises'),
(20701, 'Tips for Data Analysts');

INSERT INTO page_likes (user_id, page_id, liked_date) VALUES
(111, 20001, '2022-04-08 00:00:00'),
(121, 20045, '2022-03-12 00:00:00'),
(156, 20001, '2022-07-25 00:00:00');
""")

conexion.commit()  # Guardar cambios

# Cerrar la conexión
cur.close()
conexion.close()
