import reflex as rx

def quien_soy():
    return rx.vstack(
        rx.heading("Quién Soy", size="lg", margin_bottom="1em"),
        rx.hstack(
            # Contenedor de la imagen
            rx.box(
                rx.image(
                    src="https://i.ibb.co/q3MnTrT9/Portafolio-yo.jpg",
                    width="600px",
                    height="900px",
                    object_fit="cover",
                    border_radius="10px",
                    alt="Foto de perfil de Daniel",
                ),
                margin_right="2em",
            ),
            # Contenedor de la descripción
            rx.box(
                rx.text(
                    """Mi nombre es Daniel. Al contrario que la mayoría de desarrolladores, encontré la tecnológia en mi fase madura.
                    Considero que es un punto de valor al considerar que puedo aportar la ilusión y el hambre de quién descubre la programación,
                    y la madurez de quién tiene paciencia para obtener resultados. Mi formación se ha realizado tanto en cursos guiados como autodidacta.
                    Estaría encantado de participar  proyectos a los que unirme y desplegar todas las habilidades que he ido obteniendo.""",
                    font_size="18px",
                    font_weight="bold",
                    font_family="'Poppins', sans-serif",
                    line_height="1.6",
                ),
                max_width="600px",
            ),
            align="center",
            padding="2em",
            background_color="#2d2d2d",
            border_radius="10px",
            margin="2em",
        ),
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
    ) 