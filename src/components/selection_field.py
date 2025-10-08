import flet as ft 
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR


def selection_field(label: str, options: list, value: str = None) -> ft.Dropdown:
    dropdown = ft.Dropdown(
        label=label,
        label_style=ft.TextStyle(color=PRIMARY_COLOR), 
        options=[ft.dropdown.Option(option) for option in options],
        value=value,
        border_color='#D3D3D3',
        border_width=1,
        border_radius=15,
        focused_border_color=PRIMARY_COLOR,
        expand=True,
    )
    
    return dropdown