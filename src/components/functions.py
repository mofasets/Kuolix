import flet as ft
from sources.colors_pallete import PRIMARY_COLOR, DEFAULT_TEXT_COLOR, DEFAULT_TEXT_SIZE, SECONDARY_COLOR


def format_content(content: dict[str, str]):
    scientific_name = content.get("scientific_name", "No se encontró descripción.")
    common_names = content.get("common_names", [])
    habitat_description = content.get("habitat_description", "No se encontró descripción.")
    specific_deseases = content.get("specific_diseases", [])

    plant_content = ft.Column([
        ft.Text(
            'Nombres Comunes:', 
            size=12, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            ', '.join(common_names), 
            size=12, 
            color="#494849",
            expand=True,
            font_family='Verdana'
        ),
        ft.Text(
            'Habitat:', 
            size=12, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            habitat_description, 
            size=12, 
            color="#494849",
            font_family='Verdana'
        ),
        ft.Text(
            'Enfermedades que trata:', 
            size=12, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            ', '.join(specific_deseases), 
            size=12, 
            color="#494849",
            font_family='Verdana'
        )
    ])
    
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
        ft.Container(
            content=plant_content,
            bgcolor=SECONDARY_COLOR,
            padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
            border_radius=15,
        )        
    ])

    return content_control
