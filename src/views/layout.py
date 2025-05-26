import flet as ft
from sources.colors_pallete import PRIMARY_COLOR

def show_logo():
    logo = ft.Image(src='img/logo.png', width=100, height=100)
    app_name = ft.Text("Kuolix", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR)
    return ft.ResponsiveRow(
        controls=[ft.Container(
            content=ft.Row([logo, app_name], 
            alignment=ft.MainAxisAlignment.CENTER),
            margin=ft.margin.only(top=40, bottom=20),
        )],
        alignment=ft.MainAxisAlignment.CENTER,
    )

logo = show_logo()