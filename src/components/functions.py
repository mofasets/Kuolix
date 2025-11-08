import flet as ft
from sources.colors_pallete import PRIMARY_COLOR, DEFAULT_TEXT_COLOR, DEFAULT_TEXT_SIZE, SECONDARY_COLOR, WARNING_TITLE_COLOR, WARNING_BG_COLOR, DEFAULT_RESPONSABILITY
from components.note_card import note_card

def format_content(content: dict[str, str]):
    scientific_name = content.get("scientific_name", "No se encontró descripción.")
    common_names = content.get("common_names", [])
    habitat_description = content.get("habitat_description", "No se encontró descripción.")
    specific_deseases = content.get("specific_diseases", [])
    usage_instructions = content.get("usage_instructions", [])
    taxonomy = content.get("taxonomy", [])
    active_ingredient = content.get("active_ingredient", [])
    references = content.get("references", [])

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
        ),
        ft.Text(
            'Modo de Empleo:', 
            size=12, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            usage_instructions, 
            size=12, 
            color="#494849",
            font_family='Verdana'
        ),
        ft.Text(
            'Taxonomia:', 
            size=12, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            taxonomy, 
            size=12, 
            color="#494849",
            font_family='Verdana'
        ),
        ft.Text(
            'Principio Activo:', 
            size=12, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            active_ingredient, 
            size=12, 
            color="#494849",
            font_family='Verdana'
        ),
        ft.Text(
            'Referencias Bibliograficas:', 
            size=12, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            '\n'.join(references), 
            size=12, 
            color="#494849",
            font_family='Verdana'
        ),
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
        ),
        note_card(
            'Advertencia',
            DEFAULT_RESPONSABILITY, 
            WARNING_TITLE_COLOR, 
            WARNING_BG_COLOR, 
            ft.Icons.WARNING_AMBER
        ),

    ])

    return content_control
