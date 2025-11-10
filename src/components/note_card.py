import flet as ft 
from sources.colors_pallete import PRIMARY_COLOR, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR, SECONDARY_COLOR

def note_card(title: str, text: str, title_color: str, bg_color: str, icon: ft.Icons) -> ft.Container:
    content=ft.Column([
        ft.Row([
            ft.Icon(name=icon, color=title_color),
            ft.Text(title, size=12, color=title_color, font_family='Verdana', weight=ft.FontWeight.BOLD),
        ]),
        ft.Text(text, size=12, color="#494849", font_family='Verdana'),
    ],
        spacing=0
    )
    
    info_badge = ft.Container(
        content=content,
        bgcolor=bg_color,
        padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
        border_radius=15,
        margin=ft.margin.only(left=10, right=10)

    )
    return info_badge