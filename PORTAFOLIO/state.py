import reflex as rx
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class GlobalState(rx.State):
    is_authenticated: bool = False
    username: str = ""
    password: str = ""
    error: str = ""

    def login(self):
        admin_username = "admin"
        admin_password = "admin"
        
        if self.username == admin_username and self.password == admin_password:
            self.is_authenticated = True
            self.error = ""
            return rx.redirect("/admin")
        else:
            self.error = "Usuario o contraseña incorrectos"

    def logout(self):
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        return rx.redirect("/") 