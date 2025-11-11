import flet as ft
import time
import base64
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR, PRIMARY_TEXT_COLOR, SECONDARY_TEXT_COLOR
from sources.select_option import GENDER
from components.input_field import input_field
from components.selection_field import selection_field
from components.loading import get_loading_control
import datetime
from components.logo import logo
from components.nav_bar import nav_bar
import asyncio
from state import AppState
from typing import List
import httpx

class UserIndexView(ft.View):
    """
    Clase que encapsula la vista de configuración del perfil de usuario,
    permitiendo la edición y guardado de datos personales.
    """
    def __init__(self, page: ft.Page, app_state: AppState):
        super().__init__()
        self.page = page
        self.route = 'user/index'
        self.app_state = app_state
        self.scroll = ft.ScrollMode.AUTO
        self.padding = ft.padding.all(0)
        self.page.controls = [ft.Container(content=get_loading_control(self.page, "Cargando..."), expand=True)]

        self.floating_action_button = ft.FloatingActionButton(
            content=ft.Icon(name=ft.Icons.ADD, color=SECONDARY_COLOR),
            bgcolor=PRIMARY_COLOR,
            on_click=lambda _: self.page.go('/user/create')
        )

        if not  self.app_state.users_list:
            self.page.run_task(self.load_users_list)
        else:
            self.build_ui()

    def build_ui(self):
        """
        Construye la interfaz de usuario completa basándose en el estado actual.
        """
        
        self.results_container = ft.Column(
            scroll=ft.ScrollMode.AUTO, 
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH 
        )
        
        if self.app_state.users_list:
            for res in self.app_state.users_list:
                self.results_container.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(value=f'{res.get('name')}', size=20, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD),
                            ft.Text(value=f'{res.get('email')}', size=16)
                        ]),

                        shadow=ft.BoxShadow(
                            spread_radius=2,
                            blur_radius=3,
                            color="#CCCCCC",
                            offset=ft.Offset(0, 1),
                            blur_style=ft.ShadowBlurStyle.OUTER,
                        ),
                        padding=ft.padding.all(10),
                        border_radius=20,
                        on_click=lambda _, user=res: self.page.go(f'/user/edit/{user.get('_id')}')
                   )
                )
            
        self.controls.clear()
        self.controls = [
            ft.Container(content=ft.Column([
                logo,
                self.results_container
            ]),
                padding=ft.padding.only(left=15, right=15)
            ),
            nav_bar(self.page, 2)
        ]

    async def load_users_list(self):
        """
        Tarea asíncrona que llama a la API para obtener recomendaciones,
        las guarda en el estado y luego construye la UI.
        """

        users = await self.fetch_users()
        self.app_state.users_list = users
        
        self.build_ui()
        self.page.update()

    async def fetch_users(self) -> List[dict]:
        """
        Llama a la API, y devuelve la respuesta en formato JSON
        """
        # If there's no logged, it goes to sign in page.
        token = self.app_state.token
        if not token:
            self.page.go("/login")
            return []

        headers = {"Authorization": f"Bearer {token}"}        
        try:
        
            response = await self.app_state.api_client.get(
                f"/user/index", 
                headers=headers
            )
        
            response.raise_for_status()

            results_data = response.json()
            return results_data

        except httpx.HTTPStatusError as exc:
            print(f"Error de API: {exc.response.status_code} - {exc.response.text}")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la búsqueda: {e}")
        return []

