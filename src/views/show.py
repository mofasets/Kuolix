import flet as ft
from components.loading import get_loading_control

def get_show_view(img_source, title: str, description: str) -> ft.Container:

    content = ft.Column([
        ft.Image(src=img_source, )

    ])
    return show_view