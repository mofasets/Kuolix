import flet as ft
from components.loading import get_loading_control
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from components.logo import logo
import time


def get_show_view(page, control_state, img_source, title: str, description: str) -> ft.Container:

    def go_back(e):
        page.controls.clear()
        page.controls.append(logo)
        page.controls.append(control_state)
        page.update()

    button = ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back, icon_color=PRIMARY_COLOR, icon_size=30)

    content = ft.Column([
        button,
        ft.Container(
            content=ft.Container(ft.Image(src=img_source, fit=ft.ImageFit.COVER, width=200, height=200), padding=ft.padding.all(20), bgcolor=PRIMARY_COLOR, border_radius=20), 
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
        ),
        ft.Container(
            content=ft.Text(title, text_align=ft.TextAlign.CENTER, size=30, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR), 
            alignment=ft.alignment.center,
        ),
        ft.Container(
            content=ft.Text(description), 
            alignment=ft.alignment.center
        ),

    ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return ft.Container(
        content=content,
        alignment=ft.alignment.center,
        padding=ft.padding.only(left=10, right=10),
    )