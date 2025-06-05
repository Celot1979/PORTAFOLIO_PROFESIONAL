import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="PORTAFOLIO",
    env=rx.Env.DEV,
    db_url=os.getenv("DATABASE_URL"),
    frontend_port=3000,
    backend_port=8000
)