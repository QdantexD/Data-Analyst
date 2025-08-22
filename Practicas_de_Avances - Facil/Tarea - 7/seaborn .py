import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2

# Conexión y lectura de datos
try:
    conexion = psycopg2.connect(
        dbname="prueba_python",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
    df = pd.read_sql_query("SELECT * FROM job_listings;", conexion)
finally:
    if conexion:
        conexion.close()

# Detectar duplicados
duplicados = df.groupby(['company_id', 'title', 'description']).size().reset_index(name='count')
duplicados = duplicados[duplicados['count'] > 1]

if not duplicados.empty:
    # Contar duplicados por compañía
    duplicados_por_compania = duplicados.groupby('company_id')['count'].sum().reset_index()

    # Configurar estilo Seaborn
    sns.set(style="whitegrid")
    
    plt.figure(figsize=(10,6))
    ax = sns.barplot(x='company_id', y='count', data=duplicados_por_compania, palette="Blues_d")

    # Añadir etiquetas de valor encima de cada barra
    for p in ax.patches:
        ax.annotate(int(p.get_height()), (p.get_x() + p.get_width()/2., p.get_height()),
                    ha='center', va='bottom', fontsize=11, color='black')

    plt.title('Cantidad de trabajos duplicados por compañía', fontsize=14)
    plt.xlabel('Company ID', fontsize=12)
    plt.ylabel('Número de duplicados', fontsize=12)
    plt.tight_layout()

    # Guardar la figura
    plt.savefig("duplicados_por_compania_seaborn.png", dpi=300)
    plt.show()
    print("Gráfico generado y guardado como 'duplicados_por_compania_seaborn.png'.")
else:
    print("No se encontraron trabajos duplicados.")
