import flet as ft
from sources.colors_pallete import BACKGROUND_COLOR

def row_card(image_src: str, title: str, description: str) -> ft.Container:
    content = ft.Row([
        ft.Image(src=image_src, width=50, height=50),
        ft.Column([
            ft.Text(title),
            ft.Text(description)
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
        )
    )

    return row_card