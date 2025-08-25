import flet as ft 
from sources.colors_pallete import PRIMARY_COLOR,SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from components.loading import get_loading_control 
from components.row_card import row_card
from components.nav_bar import nav_bar
from components.logo import logo
import base64
import time
import asyncio
from state import AppState

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
            on_result=self.load_image
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
        description = ft.Container()
        if self.app_state.explore_img_description:
            description.content = ft.Text(
                self.app_state.explore_img_description,
                size=DEFAULT_TEXT_SIZE,
                color=DEFAULT_TEXT_COLOR,
            )


        # Similar Plants Control
        results_container = ft.Column()
        if self.app_state.explore_items:
            for item in self.app_state.explore_items:
                results_container.controls.append(
                    row_card(self.page, item['id'], item['img'], item['title'], item['desc'], back_route="/explore")
                )

        img_response = ft.Column([
            description,
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

    async def fetch_image_recognizer_async(self):
        """
        Simula una llamada a API asíncrona para reconocer una imagen.
        """
        print('Obteniendo reconocimiento de imagen...')
        await asyncio.sleep(2)
        print('Éxito.')
        
        results_data = []
        description = "Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet"
        for i in range(3):
            results_data.append({
                "id": f"planta_{i+1}", "img": "img/logo.png", "title": f"Plant #{i+1}", "desc": message
            })
        return description, results_data     

    def load_image(self, e: ft.FilePickerResultEvent):
        """
        Callback síncrono. Su única tarea es leer la imagen y
        lanzar la tarea de reconocimiento en segundo plano.
        """
        if not e.files:
            return

        selected_file = e.files[0]
        with open(selected_file.path, "rb") as f:
            img_bytes = f.read()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            self.app_state.explore_last_image_b64 = img_base64
            self.app_state.explore_items = []
            
            self.page.run_task(self.recognize_image_async)

    async def recognize_image_async(self):
        """
        Orquesta el proceso de reconocimiento: muestra la carga,
        llama a la API, guarda los resultados y reconstruye la UI.
        """

        self.build_ui()
        loading = get_loading_control(self.page, "Identificando...")
        self.controls.insert(2, loading) 
        self.page.update()

        results = await self.fetch_image_recognizer_async()
        self.app_state.explore_img_description, self.app_state.explore_items = results
        
        self.build_ui()
        self.page.update()