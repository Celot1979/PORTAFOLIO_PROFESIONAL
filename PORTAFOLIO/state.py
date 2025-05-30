import reflex as rx

class GlobalState(rx.State):
    is_authenticated: bool = False
    username: str = ""
    password: str = ""
    error: str = ""

    def login(self):
        if self.username == "will" and self.password == "Will1979€_":
            self.is_authenticated = True
            return rx.redirect("/admin/repositorios")
        else:
            self.error = "Usuario o contraseña incorrectos"
            return None

    def logout(self):
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        return rx.redirect("/login") 