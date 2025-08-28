import flet as ft
from sources.colors_pallete import PRIMARY_COLOR, DEFAULT_TEXT_COLOR, DEFAULT_TEXT_SIZE


def format_content(content: dict[str, str]):
    scientific_name = content.get("scientific_name", "No se encontró descripción.")
    common_names = content.get("common_names", [])
    habitat_description = content.get("habitat_description", "No se encontró descripción.")
    specific_deseases = content.get("specific_diseases", [])
    
    content_control = ft.Column([
        ft.Row([
            ft.Container(
                content=ft.Text(
                    scientific_name, 
                    color=PRIMARY_COLOR,
                    size=30,
                    weight=ft.FontWeight.BOLD
                ),
                margin=ft.margin.only(bottom=10),
            )],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Text(
            'Nombres Comunes: ' + ', '.join(common_names), 
            size=DEFAULT_TEXT_SIZE, 
            color=DEFAULT_TEXT_COLOR,
            expand=True
        ),
        ft.Text(
            habitat_description, 
            size=DEFAULT_TEXT_SIZE, 
            color=DEFAULT_TEXT_COLOR
        ),
        ft.Text(
            "Enfermedades que trata: " + ", ".join(specific_deseases), 
            size=DEFAULT_TEXT_SIZE, 
            color=DEFAULT_TEXT_COLOR
        )
    ])

    return content_control
