import customtkinter as ctk
# Importamos la clase de Login que creamos
from login import VentanaLogin 

if __name__ == "__main__":
    # Creamos la ventana raíz
    root = ctk.CTk()
    
    # Iniciamos la aplicación mostrando el Login primero
    app = VentanaLogin(root)
    
    root.mainloop()