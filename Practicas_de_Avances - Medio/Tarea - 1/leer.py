import psycopg2
import pandas as pd

conexion = psycopg2.connect(
    dbname="prueba_python",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)
cursor = conexion.cursor()

query = """
WITH likelihood AS (
    SELECT 
        user_type,
        prior_prob,
        thumbs_up_prob,
        POWER(thumbs_up_prob, 3) AS likelihood
    FROM netflix_users
),
posterior AS (
    SELECT 
        user_type,
        prior_prob * likelihood AS numerator
    FROM likelihood
)
SELECT 
    user_type,
    numerator / SUM(numerator) OVER () AS posterior_prob
FROM posterior;
"""

cursor.execute(query)
resultados = cursor.fetchall()
df = pd.DataFrame(resultados, columns=["user_type", "posterior_prob"])
print(df)

cursor.close()
conexion.close()
