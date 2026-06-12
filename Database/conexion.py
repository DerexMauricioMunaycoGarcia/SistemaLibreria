import pyodbc

def conectar():
    try:
        conexion = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=LAPTOP-CR684P59\\SQLEXPRESS;"
            "DATABASE=LibreriaDB;"
            "Trusted_Connection=yes;"
        )

        print("✅ Conexión exitosa")
        return conexion

    except Exception as e:
        print("❌ Error:", e)
        return None