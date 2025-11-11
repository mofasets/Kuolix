import flet as ft
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR

def input_field(label: str, value: str, input_type: str = None, placeholder: str = None, multiline: bool= False, readonly=False) -> ft.TextField:
    text_field = ft.TextField(
        label=label,
        label_style=ft.TextStyle(color=PRIMARY_COLOR),
        color=DEFAULT_TEXT_COLOR,
        border_color='#D3D3D3',
        hint_text=placeholder,
        border_width=1,
        border_radius=15,
        focused_border_color=PRIMARY_COLOR,
        value=value,
        keyboard_type=ft.KeyboardType.TEXT if input_type is None else input_type,
        expand=True,
        multiline=multiline,
        read_only=readonly
    )

    return text_field