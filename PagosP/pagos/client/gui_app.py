import tkinter as tk
import datetime
from tkinter import ttk, messagebox
from model.pro_pag import crear_tabla
from model.pro_pag import Pago, guadar, listar, editar, eliminar, obtener_id_cliente
from tkinter import StringVar

class Pago:
    def __init__(self, nombre_cliente, monto, fecha, tipo, id_cliente):
        self.nombre_cliente = nombre_cliente
        self.monto = monto
        self.fecha = fecha
        self.tipo = tipo
        self.id_cliente = id_cliente

def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width=300, height=300)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Inicio', menu=menu_inicio)

    menu_inicio.add_command(label='Crear Tabla en DB', command=crear_tabla)
    menu_inicio.add_command(label='Salir', command=root.destroy)
    
    menu_ayuda = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Ayuda', menu=menu_ayuda)
    menu_ayuda.add_command(label='Obtener Ayuda', command=mostrar_mensaje_ayuda)

def mostrar_mensaje_ayuda():
    mensaje = 'Comunicarse con francolimaa24@gmail.com'
    messagebox.showinfo('Ayuda', mensaje)
    

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=800, height=520)
        self.root = root
        self.pack(padx=5, pady=5)  # Ajusta estos valores según sea necesario
        self.id_pago = None
        self.ventana_solicitud = None

        self.campos_pago()
        self.desabilitar_campos()
        self.tabla_pagos()
        self.filtro_cliente()
        self.filtro_fecha()


        # Configuración de los filtros
        self.boton_limpiar_filtros = tk.Button(
            self, text="Limpiar Filtros", command=self.limpiar_filtros)
        self.boton_limpiar_filtros.config(
            width=15, font=('Arial', 12, 'bold'),
            fg='#DAD5D6', bg='#808080',
            cursor='hand2', activebackground='#A9A9A9')
        self.boton_limpiar_filtros.grid(row=7, column=3, padx=10, pady=5)

    # Resto del código...
        self.boton_primero = tk.Button(self, text="Primero", command=self.mostrar_primero)
        self.boton_primero.config(width=15, font=('Arial', 12, 'bold'),
                                  fg='#DAD5D6', bg='#158645',
                                  cursor='hand2', activebackground='#35BD6F')
        self.boton_primero.grid(row=7, column=2, padx=10, pady=5)

        self.boton_ultimo = tk.Button(self, text="Ultimo", command=self.mostrar_ultimo)
        self.boton_ultimo.config(width=15, font=('Arial', 12, 'bold'),
                                 fg='#DAD5D6', bg='#158645',
                                 cursor='hand2', activebackground='#35BD6F')
        self.boton_ultimo.grid(row=8, column=2, padx=10, pady=5)


    def mostrar_primero(self):
        # Obtiene los valores de los filtros
        nombre_cliente_filtro = self.mi_filtro_cliente.get().strip()
        fecha_inicio_str = self.mi_filtro_fecha_inicio.get().strip()
        fecha_fin_str = self.mi_filtro_fecha_fin.get().strip()

        # Filtra la lista de pagos
        registros_filtrados = self.lista_pagos
        if nombre_cliente_filtro:
            registros_filtrados = [p for p in registros_filtrados if nombre_cliente_filtro.lower() in p[1].lower()]

        if fecha_inicio_str and fecha_fin_str:
            try:
                fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                registros_filtrados = [p for p in registros_filtrados if fecha_inicio <= p[3] <= fecha_fin]
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Utiliza YYYY-MM-DD")

        # Muestra la tabla en orden original
        self.actualizar_tabla(registros_filtrados)

    def mostrar_ultimo(self):
        # Obtiene los valores de los filtros
        nombre_cliente_filtro = self.mi_filtro_cliente.get().strip()
        fecha_inicio_str = self.mi_filtro_fecha_inicio.get().strip()
        fecha_fin_str = self.mi_filtro_fecha_fin.get().strip()

        # Filtra la lista de pagos
        registros_filtrados = self.lista_pagos
        if nombre_cliente_filtro:
            registros_filtrados = [p for p in registros_filtrados if nombre_cliente_filtro.lower() in p[1].lower()]

        if fecha_inicio_str and fecha_fin_str:
            try:
                fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                registros_filtrados = [p for p in registros_filtrados if fecha_inicio <= p[3] <= fecha_fin]
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Utiliza YYYY-MM-DD")

        # Muestra la tabla en orden inverso
        self.actualizar_tabla(registros_filtrados[::-1])


    def limpiar_filtros(self):
        # Limpiar campos de filtros y actualizar la tabla
        self.mi_filtro_cliente.set('')
        self.mi_filtro_fecha_inicio.set('')
        self.mi_filtro_fecha_fin.set('')
        self.actualizar_tabla(self.lista_pagos)

    def campos_pago(self):
        self.label_nombre_cliente = tk.Label(self, text='Nombre Cliente: ')
        self.label_nombre_cliente.config(font=('Arial', 12, 'bold'))
        self.label_nombre_cliente.grid(row=0, column=0, padx=10, pady=10)

        self.label_monto = tk.Label(self, text='Monto: ')
        self.label_monto.config(font=('Arial', 12, 'bold'))
        self.label_monto.grid(row=1, column=0, padx=10, pady=10)

        self.label_fecha = tk.Label(self, text='Fecha: ')
        self.label_fecha.config(font=('Arial', 12, 'bold'))
        self.label_fecha.grid(row=2, column=0, padx=10, pady=10)

        self.label_tipo = tk.Label(self, text='Tipo: ')
        self.label_tipo.config(font=('Arial', 12, 'bold'))
        self.label_tipo.grid(row=3, column=0, padx=10, pady=10)

        self.mi_nombre_cliente = tk.StringVar()
        self.entry_nombre_cliente = tk.Entry(self, textvariable=self.mi_nombre_cliente)
        self.entry_nombre_cliente.config(width=50, font=('Arial', 12))
        self.entry_nombre_cliente.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.mi_monto = tk.StringVar()
        self.entry_monto = tk.Entry(self, textvariable=self.mi_monto)
        self.entry_monto.config(
            width=50, font=('Arial', 12))
        self.entry_monto.grid(
            row=1, column=1, padx=10, pady=10, columnspan=2)

        self.mi_fecha = tk.StringVar()
        self.entry_fecha = tk.Entry(self, textvariable=self.mi_fecha)
        self.entry_fecha.config(
            width=50, font=('Arial', 12))
        self.entry_fecha.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        self.mi_tipo = tk.StringVar()
        opciones_tipo = ['Efectivo', 'Transferencia']
        self.entry_tipo = ttk.Combobox(self, textvariable=self.mi_tipo, values=opciones_tipo)
        self.entry_tipo.config(width=50, font=('Arial', 12))
        self.entry_tipo.grid(row=3, column=1, padx=10, pady=10, columnspan=2)
        self.entry_tipo.set(opciones_tipo[0])

        self.boton_nuevo = tk.Button(self, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=('Arial', 12, 'bold'),
                                fg='#DAD5D6', bg='#158645',
                                cursor='hand2', activebackground='#35BD6F')
        self.boton_nuevo.grid(row=4, column=0, padx=10, pady=10)

        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_datos)
        self.boton_guardar.config(width=20, font=('Arial', 12, 'bold'),
                                  fg='#DAD5D6', bg='#1658A2',
                                  cursor='hand2', activebackground='#3586DF')
        self.boton_guardar.grid(row=4, column=1, padx=10, pady=10)

        self.boton_cancelar = tk.Button(
            self, text="Cancelar", command=self.desabilitar_campos)
        self.boton_cancelar.config(width=20, font=('Arial', 12, 'bold'),
                                   fg='#DAD5D6', bg='#BD152E',
                                   cursor='hand2', activebackground='#E15370')
        self.boton_cancelar.grid(row=4, column=2, padx=10, pady=10)


    def habilitar_campos(self):
        self.mi_nombre_cliente.set('')
        self.mi_monto.set('')
        self.mi_fecha.set('')
        self.mi_tipo.set('')

        self.entry_nombre_cliente.config(state='normal')
        self.entry_monto.config(state='normal')
        self.entry_fecha.config(state='normal')
        self.entry_tipo.config(state='normal')

        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def desabilitar_campos(self):
        self.id_pago = None

        self.mi_nombre_cliente.set('')
        self.mi_monto.set('')
        self.mi_fecha.set('')
        self.mi_tipo.set('')

        self.entry_nombre_cliente.config(state='disabled')
        self.entry_monto.config(state='disabled')
        self.entry_fecha.config(state='disabled')
        self.entry_tipo.config(state='disabled')

        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')

    
    def guardar_datos(self):
        nombre_cliente = self.mi_nombre_cliente.get()
        monto = self.mi_monto.get()
        fecha = self.mi_fecha.get()
        tipo = self.mi_tipo.get()

        # Buscar id_cliente basado en nombre_cliente
        id_cliente = obtener_id_cliente(nombre_cliente)

        if id_cliente is not None:
            # Utilizar el id_cliente en la creación del objeto Pago
            pago = Pago(nombre_cliente, monto, fecha, tipo, id_cliente)

            if self.id_pago is None:
                guadar(pago)
            else:
                editar(pago, self.id_pago)

            self.tabla_pagos()
            self.desabilitar_campos()
        else:
            messagebox.showerror("Error", "Cliente no encontrado")


    def tabla_pagos(self):
        self.lista_pagos = listar()
        self.lista_pagos.reverse()

        self.tabla = ttk.Treeview(self,
                                  column=('Nombre Cliente', 'Monto', 'Fecha', 'Tipo'))
        self.tabla.grid(row=5, column=0, columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self,
                                    orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=5, column=4, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='NOMBRE CLIENTE')
        self.tabla.heading('#2', text='MONTO')
        self.tabla.heading('#3', text='FECHA')
        self.tabla.heading('#4', text='TIPO')

        for p in self.lista_pagos:
            self.tabla.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4]))


        self.boton_editar = tk.Button(self, text="Editar", command=self.editar_datos)
        self.boton_editar.config(width=20, font=('Arial', 12, 'bold'),
                                 fg='#DAD5D6', bg='#158645',
                                 cursor='hand2', activebackground='#35BD6F')
        self.boton_editar.grid(row=6, column=0, padx=10, pady=10)

        self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar_datos)
        self.boton_eliminar.config(width=20, font=('Arial', 12, 'bold'),
                                    fg='#DAD5D6', bg='#BD152E',
                                    cursor='hand2', activebackground='#E15370')
        self.boton_eliminar.grid(row=6, column=1, padx=10, pady=10)

    def editar_datos(self):
        try:
            self.id_pago = self.tabla.item(
                self.tabla.selection())['text']
            self.nombre_cliente_pago = self.tabla.item(
                self.tabla.selection())['values'][0]
            self.monto_pago = self.tabla.item(
                self.tabla.selection())['values'][1]
            self.fecha_pago = self.tabla.item(
                self.tabla.selection())['values'][2]
            self.tipo_pago = self.tabla.item(
                self.tabla.selection())['values'][3]

            self.habilitar_campos()

            self.entry_nombre_cliente.insert(0, self.nombre_cliente_pago)
            self.entry_monto.insert(0, self.monto_pago)
            self.entry_fecha.insert(0, self.fecha_pago)
            self.entry_tipo.insert(0, self.tipo_pago)

        except:
            titulo = 'Edición de datos'
            mensaje = 'No ha seleccionado ningún registro'
            messagebox.showerror(titulo, mensaje)

    def eliminar_datos(self):
        if self.tabla.selection():
        # Mostrar ventana emergente para solicitar usuario y clave
            self.ventana_solicitud = tk.Toplevel(self.root)
            self.ventana_solicitud.title("Solicitud de Usuario y Clave")

            label_usuario = tk.Label(self.ventana_solicitud, text="Usuario:")
            label_usuario.grid(row=0, column=0, padx=10, pady=10)

            label_clave = tk.Label(self.ventana_solicitud, text="Clave:")
            label_clave.grid(row=1, column=0, padx=10, pady=10)

            entry_usuario = tk.Entry(self.ventana_solicitud)
            entry_usuario.grid(row=0, column=1, padx=10, pady=10)

            entry_clave = tk.Entry(self.ventana_solicitud, show="*")
            entry_clave.grid(row=1, column=1, padx=10, pady=10)

            boton_confirmar = tk.Button(self.ventana_solicitud, text="Confirmar",
                                    command=lambda: self.confirmar_eliminacion(entry_usuario.get(), entry_clave.get()))
            boton_confirmar.grid(row=2, column=0, columnspan=2, pady=10)
        else:
            titulo = 'Eliminar un Registro'
            mensaje = 'No ha seleccionado ningún registro'
            messagebox.showerror(titulo, mensaje)


    def confirmar_eliminacion(self, usuario, clave):
        # Poner Usuario
        # Poner Contraseña
        if usuario == "20191010" and clave == "7695":
            try:
                self.id_pago = self.tabla.item(self.tabla.selection())['text']
                eliminar(self.id_pago)
                self.tabla_pagos()
                self.id_pago = None
            except:
                titulo = 'Eliminar un Registro'
                mensaje = 'No ha seleccionado ningún registro'
                messagebox.showerror(titulo, mensaje)
            finally:
                if self.ventana_solicitud:
                    self.ventana_solicitud.destroy()
                    self.ventana_solicitud = None
        else:
            messagebox.showerror("Error", "Usuario o clave incorrectos")
            if self.ventana_solicitud:
                self.ventana_solicitud.destroy()
                self.ventana_solicitud = None

    def filtro_cliente(self):
        self.label_filtro_cliente = tk.Label(self, text='Filtrar por Cliente:')
        self.label_filtro_cliente.config(font=('Arial', 12, 'bold'))
        self.label_filtro_cliente.place(x=10, y=525)  # Ajusta los valores de x e y

        self.mi_filtro_cliente = tk.StringVar()
        self.entry_filtro_cliente = tk.Entry(self, textvariable=self.mi_filtro_cliente)
        self.entry_filtro_cliente.config(width=20, font=('Arial', 12))
        self.entry_filtro_cliente.place(x=150, y=525)  # Ajusta los valores de x e y

        self.boton_filtrar = tk.Button(self, text="Filtrar", command=self.filtrar_por_cliente)
        self.boton_filtrar.config(width=7, font=('Arial', 12, 'bold'),
                                  fg='#DAD5D6', bg='#158645',
                                  cursor='hand2', activebackground='#35BD6F')
        self.boton_filtrar.grid(row=7, column=1, padx=2, pady=5)

    def filtrar_por_cliente(self):
        nombre_cliente_filtro = self.mi_filtro_cliente.get().strip()
        if nombre_cliente_filtro:
            registros_filtrados = [p for p in self.lista_pagos if nombre_cliente_filtro.lower() in p[1].lower()]
            registros_filtrados.sort(key=lambda x: x[3], reverse=True)  # Ordenar por fecha
            self.actualizar_tabla(registros_filtrados)
        else:
            self.actualizar_tabla(self.lista_pagos)

    def actualizar_tabla(self, registros):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for p in registros:
            self.tabla.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4]))

        self.boton_editar.config(state=tk.DISABLED)
        self.boton_eliminar.config(state=tk.DISABLED)
        self.tabla.bind("<ButtonRelease-1>", self.habilitar_botones)

    def filtro_fecha(self):
        # Ajusta los valores de y para posicionarlo más abajo
        y_position = 565
        
        self.label_filtro_fecha_inicio = tk.Label(self, text='Desde:')
        self.label_filtro_fecha_inicio.config(font=('Arial', 12, 'bold'))
        self.label_filtro_fecha_inicio.place(x=5, y=y_position)

        self.mi_filtro_fecha_inicio = tk.StringVar()
        self.entry_filtro_fecha_inicio = tk.Entry(self, textvariable=self.mi_filtro_fecha_inicio)
        self.entry_filtro_fecha_inicio.config(width=12, font=('Arial', 12))
        self.entry_filtro_fecha_inicio.place(x=65, y=y_position)

        self.label_filtro_fecha_fin = tk.Label(self, text='Hasta:')
        self.label_filtro_fecha_fin.config(font=('Arial', 12, 'bold'))
        self.label_filtro_fecha_fin.place(x=180, y=y_position)

        self.mi_filtro_fecha_fin = tk.StringVar()
        self.entry_filtro_fecha_fin = tk.Entry(self, textvariable=self.mi_filtro_fecha_fin)
        self.entry_filtro_fecha_fin.config(width=12, font=('Arial', 12))
        self.entry_filtro_fecha_fin.place(x=235, y=y_position)

        self.boton_filtrar_fecha = tk.Button(self, text="Filtrar", command=self.filtrar_por_fecha)
        self.boton_filtrar_fecha.config(width=7, font=('Arial', 12, 'bold'),
                                    fg='#DAD5D6', bg='#158645',
                                    cursor='hand2', activebackground='#35BD6F')
        self.boton_filtrar_fecha.grid(row=8, column=1, padx=1, pady=2)

    def filtrar_por_fecha(self):
        fecha_inicio_str = self.mi_filtro_fecha_inicio.get().strip()
        fecha_fin_str = self.mi_filtro_fecha_fin.get().strip()

        try:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()

            registros_filtrados = [p for p in self.lista_pagos if fecha_inicio <= p[3] <= fecha_fin]
            registros_filtrados.sort(key=lambda x: x[3], reverse=True)  # Ordenar por fecha
            self.actualizar_tabla(registros_filtrados)
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Utiliza YYYY-MM-DD")


    def habilitar_botones(self, event):
    # Habilitar botones solo si hay una selección en la tabla
        seleccion = self.tabla.selection()
        if seleccion:
            self.boton_editar.config(state=tk.NORMAL)
            self.boton_eliminar.config(state=tk.NORMAL)
        else:
            self.boton_editar.config(state=tk.DISABLED)
            self.boton_eliminar.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Registro de Pagos")
    root.geometry("1200x700")
    app = Frame(root)
    barra_menu(root)
    root.mainloop()