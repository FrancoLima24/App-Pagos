import tkinter as tk
from client.gui_app import Frame, barra_menu

def main():
    root = tk.Tk()

    # Utiliza una ruta directa al archivo ICO
    icon_path = "C:\\Users\\Asus x515\\Desktop\\ProPa\\PagosP\\pagos\\img\\cp-logo.ico"

    try:
        # Intenta establecer el icono de la ventana principal
        root.iconbitmap(default=icon_path)
    except tk.TclError:
        # Si no puede establecer el icono, imprime un mensaje y continúa
        print(f"No se pudo establecer el icono: {icon_path}")

    root.title('Ingresar Pagos')
    root.resizable(0, 0)

    barra_menu(root)

    app = Frame(root=root)
    app.mainloop()

if __name__ == '__main__':
    main()
