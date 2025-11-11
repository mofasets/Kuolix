import flet as ft
from components.loading import get_loading_control
from sources.colors_pallete import PRIMARY_COLOR
from components.logo import logo
import time
import httpx
from state import AppState
from components.functions import format_content
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_BASE_URL")


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
        self.padding = ft.padding.all(0)

        self.loading_control = get_loading_control(self.page, "Cargando detalles...")
        self.controls = [self.loading_control]
        
        self.page.run_task(self.fetch_and_display_data)

    async def fetch_details_from_api_async(self, item_id: str) -> dict:
        """
        Realiza una llamada a la API para obtener los detalles de una planta por su ID.
        """
        
        token = self.app_state.token
        if not token:
            self.page.go("/login")
            return {}

        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = await self.app_state.api_client.get(
                f"/show/{item_id}", 
                headers=headers
            )
            response.raise_for_status()
            
            print("Detalles recibidos con éxito.")
            return response.json()

        except httpx.HTTPStatusError as exc:
            print(f"Error de API: {exc.response.status_code} - {exc.response.text}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
        
        # En caso de error, devuelve un objeto por defecto para no romper la UI.
        return {
            "scientific_name": response.get('scientific_name', 'Sin Información'),
            "common_names": response.get('common_names',[]),
            "habitat_description": response.get('habitat_description','Sin Información'),
            "specific_deseases": response.get('specific_deseases',[]),
            "usage_instructions": response.get('usage_instructions','Sin Información'),
            "taxonomy": response.get('taxonomy',[]),
            "image": f"{API_URL}/static/images/plants/{response.get('image_filename','no-image.jpg')}",
        }

    async def fetch_and_display_data(self):
        """
        Busca los datos del elemento y construye la UI final.
        """
        data = await self.fetch_details_from_api_async(self.item_id)
        
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
                    src=f"{API_URL}/static/images/plants/{data.get('image_filename','img/logo.png')}", 
                    
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

        control_content = format_content(data)

        content_column = ft.Column([
            back_button,
            image_display,
            control_content
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.START)
        
        self.controls.clear()
        self.controls.append(ft.Container(content=content_column, padding=ft.padding.only(top=20)))

    async def go_back(self, e):
        """
        Navega a la vista anterior en la pila de vistas.
        """
        if len(self.page.views) > 1:
            previous_view_route = self.page.views[-2].route
            self.page.go(previous_view_route)
        else:
            self.page.go("/explore")