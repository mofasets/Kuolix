import flet as ft
from components.loading import get_loading_control
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from components.logo import logo
import time
from state import AppState
import asyncio

async def get_details_by_id(item_id: str):
    """
    Simula una llamada a una API para obtener los detalles de un elemento.
    """
    print(f"Buscando detalles para el ID: {item_id}...")
    await asyncio.sleep(1) # Simula la espera de la red
    
    # Datos de ejemplo.
    mock_database = {
        "planta_1": {
            "title": "Cactus de Navidad",
            "image": "img/logo.png", # Asegúrate de tener estas imágenes
            "description": "El cactus de Navidad es una planta popular de interior que florece en invierno y es conocida por sus flores de colores vivos que aparecen justo a tiempo para las fiestas."
        },
        "planta_2": {
            "title": "Orquídea Phalaenopsis",
            "image": "img/logo.png",
            "description": "Conocida como orquídea mariposa, es una de las más fáciles de cuidar en casa, apreciada por sus elegantes flores que pueden durar varios meses."
        },
        "planta_3": {
            "title": "Monstera Deliciosa",
            "image": "img/logo.png",
            "description": "También llamada Costilla de Adán, es famosa por sus grandes hojas perforadas. Es una planta tropical resistente y de crecimiento rápido que añade un toque exótico a cualquier espacio."
        }
    }
    return mock_database.get(item_id, {
        "title": "Elemento no encontrado",
        "image": "img/logo.png",
        "description": "No se encontraron detalles para el ID proporcionado."
    })

class ShowView(ft.View):
    """
    Clase que encapsula la vista de detalles de un elemento específico,
    mostrando una imagen, título y descripción. Los datos se obtienen
    de la sesión de la página.
    """
    def __init__(self, page: ft.Page, item_id: str, app_state: AppState):
        super().__init__()
        self.page = page
        self.item_id = item_id
        self.app_state = app_state

        # --- Propiedades de la vista ---
        self.route = f"/show/{self.item_id}"
        self.scroll = ft.ScrollMode.AUTO

        self.loading_control = get_loading_control(self.page, "Cargando detalles...")
        self.controls = [self.loading_control]
        
        self.page.run_task(self.fetch_and_display_data)

    async def fetch_and_display_data(self):
        """
        Busca los datos del elemento y construye la UI final.
        """
        # # El "truco" para que la UI se actualice y muestre la carga.
        # await asyncio.sleep(0.01)

        data = await get_details_by_id(self.item_id)
        
        self.build_ui(data)
        self.page.update()

    def build_ui(self, data: dict):
        """
        Construye la interfaz de usuario con los datos proporcionados.
        """
        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK, 
            on_click=self.go_back, 
            icon_color=PRIMARY_COLOR, 
            icon_size=30
        )

        image_display = ft.Container(
            content=ft.Container(
                content=ft.Image(
                    src=data.get("image", "img/logo.png"), 
                    
                    fit=ft.ImageFit.COVER, 
                    width=250, 
                    height=250,
                    border_radius=20
                ), 
                padding=ft.padding.all(10), 
                bgcolor=PRIMARY_COLOR, 
                border_radius=25
            ), 
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
        )

        title_text = ft.Container(
            content=ft.Text(
                data.get("title", "Sin Título"),
                text_align=ft.TextAlign.CENTER, 
                size=30, 
                weight=ft.FontWeight.BOLD, 
                color=PRIMARY_COLOR
            ), 
            alignment=ft.alignment.center,
        )

        description_text = ft.Container(
            content=ft.Text(data.get("description", "No disponible."), text_align=ft.TextAlign.JUSTIFY), 
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=15)
        )   

        content_column = ft.Column([
            back_button,
            image_display,
            title_text,
            description_text,
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.START)
        
        self.controls.clear()
        self.controls.append(content_column)

    def go_back(self, e):
        """
        Navega a la vista anterior en la pila de vistas.
        """
        if len(self.page.views) > 1:
            previous_view_route = self.page.views[-2].route
            self.page.go(previous_view_route)
        else:
            self.page.go("/explore")