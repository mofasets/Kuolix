import flet as ft
from sources.colors_pallete import BACKGROUND_COLOR, PRIMARY_COLOR
from views.show import ShowView
from components.functions import format_content

def row_card(page: ft.Page, content: dict[str, str], back_route: str) -> ft.Container:
    def on_click(e):
        # Guardar los datos de esta tarjeta en la sesión de la página
        page.session.set("id", content.get("id"))
        page.session.set("scientific_name", content.get("scientific_name"))
        page.session.set("common_names", content.get("common_names"))
        page.session.set("habitat_description", content.get("habitat_description"))
        page.session.set("specific_deseases", content.get("specific_deseases"))
        page.session.set("back_route", back_route)
        page.go(f'/show/{content.get('id')}')
    
    control_content = ft.Row([
        ft.Image(src='img/logo.png', width=50, height=50),
        ft.Column([
            ft.Text(content.get('scientific_name'), color=PRIMARY_COLOR, size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f'{content.get('habitat_description')[:20]}...')
        ], 
            expand=True,
        )],
        spacing=20
    )

    row_card = ft.Container(
        content=control_content,
        padding=ft.padding.all(20),
        border_radius=15,
        margin=ft.margin.only(bottom=10),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=1,
            color=ft.Colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        on_click=on_click,

    )

    return row_card