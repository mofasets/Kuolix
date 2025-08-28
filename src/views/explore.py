import flet as ft 
from sources.colors_pallete import PRIMARY_COLOR,SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from components.loading import get_loading_control 
from components.row_card import row_card
from components.nav_bar import nav_bar
from components.logo import logo
from components.functions import format_content

import base64
import time
import asyncio
from state import AppState
import os
import mimetypes


message = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

class ExploreView(ft.View):
    """
    Una clase que encapsula la vista de exploración, manejo de carga de imágenes
    y visualización de resultados de reconocimiento.
    """
    def __init__(self, page: ft.Page, app_state: AppState):
        super().__init__()

        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.app_state = app_state
        self.route = "/explore"

        # Controls
        self.loaded_image = ft.Container(
            content=ft.Text(DEFAULT_TEXT, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR),
            margin=ft.margin.only(top=20, bottom=20),
            border_radius=20,
            alignment=ft.alignment.center,
        )

        self.file_picker = ft.FilePicker(
            on_result=self.recognize_image_async
        )

        self.page.overlay.append(self.file_picker)

        self.floating_action_button = ft.FloatingActionButton(
            content=ft.Icon(name=ft.Icons.UPLOAD_FILE, color=SECONDARY_COLOR),
            bgcolor=PRIMARY_COLOR,
            on_click=lambda _: self.file_picker.pick_files(
                allow_multiple=False, # Es mejor ser explícito
                file_type=ft.FilePickerFileType.IMAGE
            )
        )
        self.build_ui()

    def build_ui(self):
        """
        Construye la interfaz de usuario de la vista basándose en el estado actual.
        """
        if self.app_state.explore_last_image_b64:
            image_content = ft.Image(
                src_base64=self.app_state.explore_last_image_b64,
                width=200, height=200, border_radius=20, fit=ft.ImageFit.COVER
            )
        else:
            image_content = ft.Text(DEFAULT_TEXT, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR)

        # Image Control
        self.loaded_image = ft.Container(
            content=image_content,
            margin=ft.margin.only(top=20, bottom=20),
            border_radius=20,
            alignment=ft.alignment.center,
        )

        # Description Control.
        description = ft.Container(margin=ft.margin.only(bottom=20))
        if self.app_state.explore_img_description:
            description.content = format_content(self.app_state.explore_img_description)

        similar_plants_title = ft.Container(margin=ft.margin.only(bottom=10))
        if self.app_state.explore_items:
            similar_plants_title.content = ft.Text('Plantas Similares', size=20, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD)

        # Similar Plants Control
        results_container = ft.Column()
        if self.app_state.explore_items:
            for item in self.app_state.explore_items:
                results_container.controls.append(
                    row_card(self.page, item, back_route="/explore")
                )

        img_response = ft.Column([
            description,
            similar_plants_title,
            results_container,
        ])

        self.controls = [
            logo,
            self.loaded_image,
            ft.Container(
                content=img_response,
                alignment=ft.alignment.center,
                padding=ft.padding.all(10),
            ),
            nav_bar(self.page, 0)
        ]

    async def fetch_image_recognizer_async(self, image_path: str):
        """
        Simula una llamada a API asíncrona para reconocer una imagen.
        """

        print(f"Iniciando reconocimiento para la imagen: {image_path}")
        
        token = self.app_state.token
        if not token:
            print("Error: No se encontró token de autenticación.")
            self.page.go("/login")
            return "Error de autenticación", []

        headers = {"Authorization": f"Bearer {token}"}

        try:
            file_name = os.path.basename(image_path)
            content_type = mimetypes.guess_type(image_path)[0] or 'application/octet-stream'

            with open(image_path, "rb") as image_file:
                files_to_upload = {"img": (file_name, image_file, content_type)}
                
                print("Enviando imagen a la API...")
                response = await self.app_state.api_client.post(
                    "/explore/recognize_img",
                    files=files_to_upload,
                    headers=headers
                )
                response.raise_for_status()
                
                data = response.json()
                print("Respuesta recibida de la API.")

                # Mapeamos la respuesta al formato que la UI espera
                item_info = data.get("img_result", {})
                results_data = data.get("suggested_plants", [])
                
                return item_info, results_data

        except Exception as e:
            print(f"Ocurrió un error al llamar a la API: {e}")
            return f"Error: {e}", []

    async def recognize_image_async(self, e: ft.FilePickerResultEvent):
        """
        Orquesta el proceso de reconocimiento: muestra la carga,
        llama a la API, guarda los resultados y reconstruye la UI.
        """
        if not e.files:
            return

        selected_file_path = e.files[0].path
        with open(selected_file_path, "rb") as f:
            img_bytes = f.read()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            self.app_state.explore_last_image_b64 = img_base64
            self.app_state.explore_img_description = {}
            self.app_state.explore_items = []
        
        self.build_ui()
        loading = get_loading_control(self.page, "Identificando...")
        self.controls.insert(2, loading) 
        self.page.update()

        results = await self.fetch_image_recognizer_async(selected_file_path)
        self.app_state.explore_img_description, self.app_state.explore_items = results
        
        self.build_ui()
        self.page.update()


