import flet as ft
from sources.colors_pallete import BACKGROUND_COLOR
from views.show import ShowView


def row_card(page: ft.Page, id: str, image_src: str, title: str, description: str, back_route: str) -> ft.Container:
    def on_click(e):
        # Guardar los datos de esta tarjeta en la sesión de la página
        page.session.set("id", id)
        page.session.set("show_image_src", image_src)
        page.session.set("show_title", title)
        page.session.set("show_description", description)
        page.session.set("back_route", back_route) # Guardar la ruta para poder volver
        page.go(f'/show/{id}')
    
    content = ft.Row([
        ft.Image(src=image_src, width=50, height=50),
        ft.Column([
            ft.Text(title),
            ft.Text(f'{description[:20]}...')
        ], 
            expand=True,
        )],
        spacing=20
    )

    row_card = ft.Container(
        content=content,
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