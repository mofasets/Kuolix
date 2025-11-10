import flet as ft
from sources.colors_pallete import (
    PRIMARY_COLOR, 
    SECONDARY_COLOR, 
    WARNING_TITLE_COLOR, 
    WARNING_BG_COLOR, 
    DEFAULT_RESPONSABILITY,
    DEFAULT_DANGER,
    DANGER_TITLE_COLOR,
    DARGER_BG_COLOR
)
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
            size=16, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            ', '.join(common_names), 
            size=16, 
            color="#494849",
            expand=True,
            font_family='Verdana'
        ),
        ft.Text(
            'Habitat:', 
            size=16, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            habitat_description, 
            size=16, 
            color="#494849",
            font_family='Verdana'
        ),
        ft.Text(
            'Enfermedades que trata:', 
            size=16, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            ', '.join(specific_deseases), 
            size=16, 
            color="#494849",
            font_family='Verdana'
        ),
        ft.Text(
            'Modo de Empleo:', 
            size=16, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            usage_instructions, 
            size=16, 
            color="#494849",
            font_family='Verdana'
        ),
        ft.Text(
            'Taxonomia:', 
            size=16, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            taxonomy, 
            size=16, 
            color="#494849",
            font_family='Verdana'
        ),
        ft.Text(
            'Principio Activo:', 
            size=16, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            active_ingredient, 
            size=16, 
            color="#494849",
            font_family='Verdana'
        ),
        ft.Text(
            'Referencias Bibliograficas:', 
            size=16, 
            color="#494849",
            font_family='Verdana',
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            '\n'.join(references), 
            size=16, 
            color="#494849",
            font_family='Verdana'
        ),
    ])
    
    #Add note card based on safety_level plant field.
    safety_level = content.get("safety_level", False)
    plant_note_card = None

    if content.get("safety_level") and safety_level == 'Toxic':
        plant_note_card = note_card(
            'Cuidado!',
            DEFAULT_DANGER,
            DANGER_TITLE_COLOR,
            DARGER_BG_COLOR,
            ft.Icons.WARNING_AMBER
        )
    else:
        plant_note_card = note_card(
            'Advertencia',
            DEFAULT_RESPONSABILITY, 
            WARNING_TITLE_COLOR, 
            WARNING_BG_COLOR, 
            ft.Icons.WARNING_AMBER
        )

    content_control = ft.Column([
        ft.Row([
            ft.Container(
                content=ft.Text(
                    scientific_name, 
                    color=PRIMARY_COLOR,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
                margin=ft.margin.only(bottom=10),
                alignment=ft.alignment.center
            )],
            wrap=True
        ),
        plant_note_card,
        ft.Container(
            content=plant_content,
            bgcolor=SECONDARY_COLOR,
            padding=ft.padding.all(20),
            margin=ft.margin.only(left=10, right=10),
            border_radius=15,
        )
    ])

    return content_control
