import pyodbc

server = 'localhost'  # ou 'localhost\\SQLEXPRESS' se for instância nomeada
database = 'AdventureWorks2022'
username = 'SEU_USUARIO_AQUI'
password = 'SUA_SENHA_AQUI'
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Conexão Python–SQL bem-sucedida!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 5 Name, ListPrice FROM Production.Product;")
    for row in cursor.fetchall():
        print(row)
    
    conn.close()
except Exception as e:
    print("❌ Erro de conexão:", e)
