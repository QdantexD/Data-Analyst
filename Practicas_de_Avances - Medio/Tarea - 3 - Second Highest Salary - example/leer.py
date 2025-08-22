import psycopg2
import pandas as pd

# Conexión a PostgreSQL
conexion = psycopg2.connect(
    dbname="prueba_python",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)
cursor = conexion.cursor()

# -------------------------------
# Ejecutar consulta del segundo salario más alto (DISTINCT + OFFSET)
# -------------------------------
query = """
SELECT DISTINCT salary AS second_highest_salary
FROM employee
ORDER BY salary DESC
OFFSET 1 LIMIT 1;
"""
cursor.execute(query)
resultados = cursor.fetchall()
df = pd.DataFrame(resultados, columns=["second_highest_salary"])
print("Usando DISTINCT + OFFSET:")
print(df, "\n")

# -------------------------------
# Ejecutar consulta con DENSE_RANK
# -------------------------------
query2 = """
WITH ranked AS (
    SELECT 
        salary,
        DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employee
)
SELECT salary AS second_highest_salary
FROM ranked
WHERE rnk = 2;
"""
cursor.execute(query2)
resultados2 = cursor.fetchall()
df2 = pd.DataFrame(resultados2, columns=["second_highest_salary"])
print("Usando DENSE_RANK:")
print(df2)

# Cerrar conexión
cursor.close()
conexion.close()
