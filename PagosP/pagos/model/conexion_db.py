import pyodbc

class ConexionDB:
    def __init__(self):
        # Configura tus credenciales y detalles de conexión para SQL Server
        server = 'localhost'
        database = 'BaseP'
        username = 'sa'
        password = 'mercadolibre98'
        driver = '{ODBC Driver 17 for SQL Server}'  # Asegúrate de tener el controlador correcto

        # Construye la cadena de conexión
        connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        # Conéctate a la base de datos SQL Server
        self.conexion = pyodbc.connect(connection_string)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        # Cierra la conexión y realiza la confirmación de los cambios
        self.conexion.commit()
        self.conexion.close()
