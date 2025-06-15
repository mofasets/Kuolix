import flet as ft 
from sources.colors_pallete import PRIMARY_COLOR, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR


def get_loading_control(page: ft.Page, text: str) -> ft.Column:

    #Controls
    loading_spinner = ft.Container(
        content=ft.ProgressRing(color=PRIMARY_COLOR, width=40, height=40),
        alignment=ft.alignment.center,
        margin=ft.margin.only(top=50),
    )

    loading_control=ft.Column([
        loading_spinner,
        ft.Container(
            content=ft.Text(text, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR), 
            alignment=ft.alignment.center
        ),
    ])

    return loading_control

