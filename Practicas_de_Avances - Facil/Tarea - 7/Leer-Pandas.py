import pandas as pd
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

# Ejecutamos la consulta
cursor.execute("SELECT * FROM job_listings;")
datos = cursor.fetchall()

# Convertir a DataFrame
columnas = [desc[0] for desc in cursor.description]  # toma los nombres de columnas
df = pd.DataFrame(datos, columns=columnas)

print(df)

# Agrupar por company_id, title y description, y contar
duplicados = df.groupby(['company_id', 'title', 'description']).size().reset_index(name='count')

# Filtrar solo los que tienen más de 1
duplicados = duplicados[duplicados['count'] > 1]

# Contar compañías únicas con duplicados
num_companies = duplicados['company_id'].nunique()
print("Cantidad de compañías con trabajos duplicados:", num_companies)
