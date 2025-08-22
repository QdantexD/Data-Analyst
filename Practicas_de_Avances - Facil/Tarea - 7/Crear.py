import psycopg2

# Conexión
conexion = psycopg2.connect(
    dbname="prueba_python",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)
cursor = conexion.cursor()

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS job_listings (
    job_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    title TEXT,
    description TEXT
);
""")
conexion.commit()

# Datos de ejemplo
jobs = [
    (248, 827, "Business Analyst", "Business analyst evaluates past and current business data with the primary goal of improving decision-making processes within organizations."),
    (149, 845, "Business Analyst", "Business analyst evaluates past and current business data with the primary goal of improving decision-making processes within organizations."),
    (945, 345, "Data Analyst", "Data analyst reviews data to identify key insights into a business's customers and ways the data can be used to solve problems."),
    (164, 345, "Data Analyst", "Data analyst reviews data to identify key insights into a business's customers and ways the data can be used to solve problems."),
    (172, 244, "Data Engineer", "Data engineer works in a variety of settings to build systems that collect, manage, and convert raw data into usable information for data scientists and business analysts to interpret.")
]

# Insertar datos
insert_query = "INSERT INTO job_listings (job_id, company_id, title, description) VALUES (%s, %s, %s, %s) ON CONFLICT (job_id) DO NOTHING;"
cursor.executemany(insert_query, jobs)
conexion.commit()

# Consulta SQL
duplicate_query = """
SELECT COUNT(DISTINCT company_id) AS duplicate_companies
FROM (
    SELECT company_id, title, description, COUNT(*) AS cnt
    FROM job_listings
    GROUP BY company_id, title, description
    HAVING COUNT(*) > 1
) AS duplicates;
"""

cursor.execute(duplicate_query)
result = cursor.fetchone()
print("Cantidad de compañías con trabajos duplicados:", result[0])

cursor.close()
conexion.close()

