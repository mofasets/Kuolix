import flet as ft
import time
import base64
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DANGER_TITLE_COLOR, DARGER_BG_COLOR
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
        self.confirm_dialog: ft.AlertDialog = None
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
                        content=ft.Row([
                            ft.Column([
                                ft.Text(value=f'{res.get('name')}', size=20, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD),
                                ft.Text(value=f'{res.get('email')}', size=16)
                            ], expand=True),
                            ft.Column([
                                ft.IconButton(
                                    icon=ft.Icons.DELETE, 
                                    icon_color=DANGER_TITLE_COLOR, 
                                    bgcolor=DARGER_BG_COLOR,
                                    on_click=lambda e, item_id=res.get('_id'), item_name=res.get('name'): self.open_delete_dialog(item_id, item_name)
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.END)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                        shadow=ft.BoxShadow(
                            spread_radius=2,
                            blur_radius=3,
                            color="#CCCCCC",
                            offset=ft.Offset(0, 1),
                            blur_style=ft.ShadowBlurStyle.OUTER,
                        ),
                        padding=ft.padding.all(10),
                        border_radius=20,
                        on_click=lambda _, user=res: self.page.go(f'/user/edit/{user.get('_id')}'),
                        margin=ft.margin.only(bottom=30)
                   )
                )
            
        self.controls.clear()
        self.controls = [
            ft.Container(content=ft.Column([
                ft.Row([
                    ft.IconButton(icon=ft.Icons.LOGOUT, on_click=self.logout, icon_color=PRIMARY_COLOR)], 
                    alignment=ft.MainAxisAlignment.END,
                ),
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

    def open_delete_dialog(self, item_id: str, item_name: str):
        """
        Construye y muestra el modal de confirmación de borrado.
        """
        print(f"Abriendo diálogo para borrar {item_name}")
        
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Está seguro de que desea eliminar el registro de '{item_name}'?\n\nEsta acción no se puede deshacer."),
            actions=[
                ft.TextButton(
                    "No, Cancelar",
                    on_click=self.close_dialog # Llama a la función de cierre
                ),
                ft.TextButton(
                    "Sí, Eliminar",
                    style=ft.ButtonStyle(color=ft.Colors.RED_500),
                    on_click=lambda e, id=item_id: self.page.run_task(self.delete_record_confirmed,id) 
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.open(self.confirm_dialog)
        
        self.confirm_dialog.open = True
        self.page.update()

    async def close_dialog(self, e: ft.ControlEvent = None):
        """Cierra el modal de diálogo actual."""
        if self.confirm_dialog:
            self.confirm_dialog.open = False
            self.page.update()

    async def delete_record_confirmed(self, item_id: str):
        """
        Esta es la función que realmente llama a tu API para borrar.
        """
        token = self.app_state.token
        if not token:
            self.page.go("/login")
            await self.close_dialog()
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = await self.app_state.api_client.delete(
                f"/user/delete/{item_id}", 
                headers=headers
            )
            response.raise_for_status()

            self.page.open(
                ft.SnackBar(
                    ft.Text("Registro eliminado con éxito"), 
                    bgcolor=ft.Colors.GREEN_400,
                    duration=2000
                )
            )

            if self.app_state.users_list:
                self.app_state.users_list = [
                    item for item in self.app_state.users_list 
                    if item.get('_id') != item_id
                ]
            
            self.build_ui() 
            
        except httpx.HTTPStatusError as exc:
            try:
                error_detail = exc.response.json().get("detail", "Error de servidor")
            except:
                error_detail = exc.response.text
                print(f'Error encontrado: {error_detail}')
            self.page.open(
                ft.SnackBar(
                    ft.Text(f"Error de API: {error_detail}"), 
                    bgcolor=ft.Colors.RED_400,
                    duration=3000
                )
            )
            
        except Exception as ex:
            self.page.open(
                ft.SnackBar(
                    ft.Text(f"Error de conexión: {ex}"), 
                    bgcolor=ft.Colors.RED_400,
                    duration=3000
                )
            )
            print(f'Error encontrado: {ex}')
        await self.close_dialog()
        self.page.update()        

    def logout(self, e):
        """Limpia el estado de la sesión y redirige al login."""
        self.app_state.token = None
        self.user_id = None
        self.app_state.user_profile = None
        self.app_state.explore_items = []
        self.app_state.explore_last_image_b64 = None
        self.app_state.explore_img_description = {}
        self.app_state.search_query = ""
        self.app_state.search_results = []
        print("Sesión cerrada.")
        self.page.go("/login")