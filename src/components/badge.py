import flet as ft 
from sources.colors_pallete import SECONDARY_COLOR, PRIMARY_COLOR

def badge(description: str) -> ft.Control:
    item_badge = ft.Container(
        content=ft.Text(description, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD),
        padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
        border_radius=50,
        bgcolor=SECONDARY_COLOR,
    )

    return item_badge