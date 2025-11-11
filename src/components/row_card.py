import flet as ft
from sources.colors_pallete import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR
from components.badge import badge
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
        page.session.set("specific_diseases", content.get("specific_diseases"))
        page.session.set("back_route", back_route)
        page.go(f'/show/{content.get("id")}')

    image_url = f"{API_URL}/static/images/plants/{content.get('image_filename','no-image.jpg')}"

    plant_image = ft.Image(
        src=image_url,
        fit=ft.ImageFit.COVER, 
        border_radius=ft.border_radius.all(15),
        error_content=ft.Image(
            src='img/logo.png',
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(15),
        )
    )

    # edit Button
    edit_plant_button = ft.IconButton(
        icon=ft.Icons.EDIT_NOTE, 
        icon_color=PRIMARY_COLOR, 
        bgcolor=BACKGROUND_COLOR,
        on_click=lambda _:page.go(f'/edit/{content.get("id")}')
    )

    #Badges with the specific deseases.
    specific_deseases_badges = ft.Container()
    if content.get('specific_diseases'):
        specific_deseases_badges.content = ft.Row([badge(desease) for desease in content.get('specific_diseases')], wrap=True)

    control_content = ft.Row([
        ft.Column([
            ft.Row([edit_plant_button], alignment=ft.MainAxisAlignment.END),
            ft.Container(content=plant_image, alignment=ft.alignment.center),
            ft.Text(content.get('scientific_name'), color=PRIMARY_COLOR, size=24, weight=ft.FontWeight.BOLD),
            specific_deseases_badges,
            ft.Text(f'{content.get("habitat_description", "")[:100]}...', size=16)
        ], 
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )],
        spacing=20,
    )

    row_card = ft.Container(
        content=control_content,
        padding=ft.padding.only(left=10, right=10, top=10, bottom=30),
        border_radius=15,
        margin=ft.margin.only(bottom=10),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=3,
            color="#CCCCCC",
            offset=ft.Offset(0, 1),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        on_click=on_click,
    )

    return row_card