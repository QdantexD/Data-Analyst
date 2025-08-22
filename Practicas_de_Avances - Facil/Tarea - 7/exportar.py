import pandas as pd
import psycopg2
from psycopg2 import OperationalError

try:
    # Conexión
    conexion = psycopg2.connect(
        dbname="prueba_python",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
except OperationalError as e:
    print("Error conectando a PostgreSQL:", e)
    raise

try:
    cursor = conexion.cursor()
    cursor.execute("SELECT job_id, company_id, title, description FROM job_listings;")
    datos = cursor.fetchall()

    # Columnas desde cursor.description
    columnas = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(datos, columns=columnas)

    # Guardar todo
    df.to_excel("job_listings.xlsx", index=False)
    print("Archivo creado: job_listings.xlsx")

    # Detectar duplicados (agrupando)
    duplicados = (df
                  .groupby(['company_id', 'title', 'description'])
                  .size()
                  .reset_index(name='count'))
    duplicados = duplicados[duplicados['count'] > 1]

    # Guardar duplicados
    duplicados.to_excel("duplicados.xlsx", index=False)
    print("Archivo creado: duplicados.xlsx")

finally:
    # Cerrar cursor y conexión de forma segura
    try:
        cursor.close()
    except Exception:
        pass
    conexion.close()
