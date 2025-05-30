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
        if (
            self.username == os.getenv("ADMIN_USERNAME", "will")
            and self.password == os.getenv("ADMIN_PASSWORD", "Will1979€_")
        ):
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