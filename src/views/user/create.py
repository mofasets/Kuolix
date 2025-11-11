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


class UserCreateView(ft.View):
    """
    Clase que encapsula la vista de configuración del perfil de usuario,
    permitiendo la edición y guardado de datos personales.
    """
    def __init__(self, page: ft.Page, app_state: AppState):
        super().__init__()
        self.page = page
        self.route = '/user/create'
        self.app_state = app_state
        self.scroll = ft.ScrollMode.AUTO
        self.padding = ft.padding.all(0)
        self.setup_controls()

        self.build_ui(self.app_state.current_user)

    def setup_controls(self):
        """Inicializa los controles interactivos vacíos."""
        self.update_button = ft.FilledButton(text='Crear Usuario', on_click=self.create_profile, bgcolor=PRIMARY_COLOR)
        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(1920, 1, 1),
            last_date=datetime.datetime.now(),
            on_change=self.handle_date_selection_change,
        )
        self.name_input = input_field('Nombre', '')
        self.email_input = input_field('Correo Electrónico', '', ft.KeyboardType.EMAIL)
        self.phone_input = input_field('Teléfono', '', ft.KeyboardType.PHONE)
        self.country_input = input_field('País', '')
        self.gender_input = selection_field('Género', GENDER)
        self.birthdate_input = input_field('Fecha de Nacimiento', '', readonly=True)
        self.password_input = input_field('Contraseña', '')

    def build_ui(self, data: dict):
        """Construye la interfaz de usuario completa con los datos del perfil."""

        form_content = ft.Column([
            self.name_input, 
            self.email_input, 
            self.phone_input, 
            self.country_input, 
            self.gender_input,
            self.password_input,

            ft.Row([
                self.birthdate_input,
                ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=lambda _: self.page.open(self.date_picker), bgcolor=SECONDARY_COLOR, icon_color=PRIMARY_COLOR)
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                self.update_button,
                ft.FilledButton(text='Cerrar', on_click=lambda _:self.page.go('/user/index'), bgcolor=SECONDARY_COLOR, color=PRIMARY_COLOR)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        ], scroll=ft.ScrollMode.AUTO, expand=True)

        content = ft.Column([
            logo,
            form_content, 
        ])

        self.controls.clear()
        self.controls.extend([
            ft.Container(content=content, padding=ft.padding.only(top=20, left=10, right=10, bottom=20)),
            nav_bar(self.page, 2),
        ])

    def handle_date_selection_change(self, e):
        """Actualiza el campo de fecha de nacimiento cuando se selecciona una fecha."""
        if self.date_picker.value:
            self.birthdate_input.value = f"{self.date_picker.value.strftime('%Y-%m-%d')}"
        else:
            self.birthdate_input.value = ""
        self.page.update()

    async def create_profile(self, e):
        """"""
        data = {
            "name": self.name_input.value,
            "email": self.email_input.value,
            "phone": self.phone_input.value,
            "country": self.country_input.value,
            "gender": self.gender_input.value,
            "birth_date": self.birthdate_input.value,
            "password": self.password_input.value
        }

        token = self.app_state.token
        if not token:
            self.page.go("/login")
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        try:
            # Llama al endpoint POST, enviando los datos como JSON
            response = await self.app_state.api_client.post(f"/user/create", json=data, headers=headers)
            response.raise_for_status()
            
            self.app_state.current_user = response.json() 
            
        except Exception as ex:
            print(ex)
            self.page.open(ft.SnackBar(content=ft.Text('Error al Actualizar Datos', color="white"), bgcolor=ft.Colors.RED_400, duration=1000))    

        self.page.open(ft.SnackBar(content=ft.Text('Perfil actualizado con éxito.', color="white"), bgcolor=ft.Colors.GREEN_400, duration=1000))
        self.update_button.disabled = False
        self.page.update()

