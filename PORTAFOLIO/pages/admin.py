import reflex as rx
from ..state import GlobalState

def admin():
    return rx.cond(
        GlobalState.is_authenticated,
        rx.vstack(
            rx.hstack(
                rx.heading("Panel de Administración", size="lg"),
                rx.spacer(),
                rx.button("Cerrar Sesión", on_click=GlobalState.logout, color_scheme="red"),
                width="100%",
                margin_bottom="2em",
            ),
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.heading("Gestión de Repositorios", size="md"),
                        rx.text("Administra tus proyectos y repositorios"),
                        rx.button(
                            "Ir a Repositorios",
                            on_click=rx.redirect("/admin/repositorios"),
                            color_scheme="blue",
                            margin_top="1em",
                        ),
                        align_items="center",
                        padding="2em",
                        border="1px solid #2d3748",
                        border_radius="lg",
                        background="rgba(255, 255, 255, 0.05)",
                        _hover={
                            "transform": "translateY(-5px)",
                            "transition": "all 0.3s ease",
                            "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                        },
                    ),
                    width="300px",
                ),
                rx.box(
                    rx.vstack(
                        rx.heading("Gestión del Blog", size="md"),
                        rx.text("Administra las entradas de tu blog"),
                        rx.button(
                            "Ir al Blog",
                            on_click=rx.redirect("/admin/blog"),
                            color_scheme="green",
                            margin_top="1em",
                        ),
                        align_items="center",
                        padding="2em",
                        border="1px solid #2d3748",
                        border_radius="lg",
                        background="rgba(255, 255, 255, 0.05)",
                        _hover={
                            "transform": "translateY(-5px)",
                            "transition": "all 0.3s ease",
                            "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                        },
                    ),
                    width="300px",
                ),
                spacing="2em",
                justify="center",
            ),
            style={
                "background_color": "#1a1a1a",
                "color": "#ffffff",
                "min_height": "100vh",
                "padding": "2em",
            },
        ),
        rx.center(
            rx.vstack(
                rx.heading("Acceso Denegado", size="lg"),
                rx.text("Por favor, inicia sesión para acceder a esta página."),
                rx.button("Ir al Login", on_click=rx.redirect("/login")),
                spacing="1em",
            ),
            width="100%",
            height="100vh",
        ),
    ) 