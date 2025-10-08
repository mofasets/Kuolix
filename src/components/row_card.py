import flet as ft
from sources.colors_pallete import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR
from views.show import ShowView
from state import app_state
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_BASE_URL")


def row_card(page: ft.Page, content: dict[str, str], back_route: str) -> ft.Container:
    def on_click(e):
        page.session.set("id", content.get("id"))
        page.session.set("scientific_name", content.get("scientific_name"))
        page.session.set("common_names", content.get("common_names"))
        page.session.set("habitat_description", content.get("habitat_description"))
        page.session.set("specific_deseases", content.get("specific_deseases"))
        page.session.set("back_route", back_route)
        page.go(f'/show/{content.get("id")}')

    image_url = f"{API_URL}/static/images/plants/{content.get('image_filename','no-image.jpg')}"

    plant_image = ft.Image(
        src=image_url,
        width=50,
        height=50,
        fit=ft.ImageFit.COVER, 
        border_radius=ft.border_radius.all(5),
        
        error_content=ft.Image(
            src='img/logo.png',
            width=50,
            height=50,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(5),
        )
    )

    control_content = ft.Row([
        plant_image, # Reemplazamos el ft.Image anterior por nuestra nueva variable
        ft.Column([
            ft.Text(content.get('scientific_name'), color=PRIMARY_COLOR, size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f'{content.get("habitat_description", "")[:30]}...')
        ], 
            expand=True,
        )],
        spacing=20
    )
    
    # --- FIN DE CAMBIOS ---

    row_card = ft.Container(
        content=control_content,
        padding=ft.padding.all(20),
        border_radius=15,
        margin=ft.margin.only(bottom=10),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=1,
            color=SECONDARY_COLOR,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        on_click=on_click,
    )

    return row_card