from .conexion_db import ConexionDB
from tkinter import messagebox

def crear_tabla():
    conexion = ConexionDB()

    sql = '''
    CREATE TABLE pagos (
        id_pagos INT IDENTITY(1,1) PRIMARY KEY,
        nombre_cliente VARCHAR(60) NOT NULL,
        monto DECIMAL(10, 2) NOT NULL,
        fecha DATE NOT NULL,
        tipo VARCHAR(50),
        id_cliente int not null,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
    );'''
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Crear Registro'
        mensaje = 'Se creó la tabla en la base de datos'
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = 'Crear Registro'
        mensaje = 'La tabla ya está creada'
        messagebox.showwarning(titulo, mensaje)

def borrar_tabla():
    conexion = ConexionDB()

    sql = 'DROP TABLE pagos'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Borrar Registro'
        mensaje = 'La tabla de la base de datos se borró con éxito'
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = 'Borrar Registro'
        mensaje = 'No hay tabla para borrar'
        messagebox.showerror(titulo, mensaje)

class Pago:
    def __init__(self, nombre_cliente, monto, fecha, tipo, id_cliente):
        self.id_pago = None
        self.nombre_cliente = nombre_cliente
        self.monto = monto
        self.fecha = fecha
        self.tipo = tipo
        self.id_cliente = id_cliente

    def __str__(self):
        return f'Pago[{self.nombre_cliente}, {self.monto}, {self.fecha}, {self.tipo}]'

def guadar(pago):
    conexion = ConexionDB()

    sql = f"""INSERT INTO pagos (nombre_cliente, monto, fecha, tipo, id_cliente)
    VALUES('{pago.nombre_cliente}', {pago.monto}, '{pago.fecha}', '{pago.tipo}', {pago.id_cliente})"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = 'Conexión al Registro'
        mensaje = 'La tabla pagos no está creada en la base de datos'
        messagebox.showerror(titulo, mensaje)



def listar():
    conexion = ConexionDB()

    lista_pagos = []
    sql = 'SELECT * FROM pagos'

    try: 
        conexion.cursor.execute(sql)
        lista_pagos = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexión al Registro '
        mensaje = 'Crea la tabla en la Base de datos'
        messagebox.showwarning(titulo, mensaje)

    return lista_pagos

def editar(pago, id_pago):
    conexion = ConexionDB()

    sql = f"""UPDATE pagos 
    SET nombre_cliente = '{pago.nombre_cliente}', monto = {pago.monto},
    fecha = '{pago.fecha}', tipo = '{pago.tipo}'
    WHERE id_pagos = {id_pago}"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()

    except:
        titulo = 'Edición de datos'
        mensaje = 'No se pudo editar este registro'
        messagebox.showerror(titulo, mensaje)

def eliminar(id_pago):
    conexion = ConexionDB()
    sql = f'DELETE FROM pagos WHERE id_pagos = {id_pago}'

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = 'Eliminar Datos'
        mensaje = 'No se pudo eliminar el registro'
        messagebox.showerror(titulo, mensaje)

def obtener_id_cliente(nombre_cliente):
    conexion = ConexionDB()

    try:
        nombre_cliente = nombre_cliente.lower()

        # Corregir la forma de pasar el valor en la consulta preparada
        conexion.cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = ?", (nombre_cliente,))
        resultado = conexion.cursor.fetchone()

        if resultado:
            id_cliente = resultado[0]
            print(f"Cliente encontrado: ID {id_cliente}")
            return id_cliente
        else:
            print("Cliente no encontrado en la base de datos.")
            return None

    except Exception as e:
        print(f"Error al obtener el id_cliente: {e}")
        return None

    finally:
        conexion.cerrar()