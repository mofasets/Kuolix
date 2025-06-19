import flet as ft
from sources.colors_pallete import BACKGROUND_COLOR
from views.show import get_show_view


def row_card(search_view, page: ft.Page, image_src: str, title: str, description: str) -> ft.Container:
    def on_click(e):
        page.controls.clear()
        page.controls.append(get_show_view(page,search_view, image_src, title, description))
        page.update()

    
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