import flet as ft
import time
import base64
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR, PRIMARY_TEXT_COLOR, SECONDARY_TEXT_COLOR
from sources.select_option import GENDER
from components.input_field import input_field
from components.selection_field import selection_field
from components.loading import get_loading_control
import datetime
from components.logo import logo
from components.nav_bar import nav_bar
import asyncio
from state import AppState


# ELIMINAR CUANDO SE INTEGRE CON EL BACKEND
DATA_EXAMPLE = {
    "name": "Sebastian Osto",
    "email": "sebastianosto1@gmail.com",
    "phone": "04241234567",
    "country": "Venezuela",
    "gender": "Masculino",
    "birthdate": "1990-01-01"
}

class SettingsView(ft.View):
    """
    Clase que encapsula la vista de configuración del perfil de usuario,
    permitiendo la edición y guardado de datos personales.
    """
    def __init__(self, page: ft.Page, app_state: AppState):
        super().__init__()
        self.page = page
        self.app_state = app_state
        # Propiedades de la vista
        self.scroll = ft.ScrollMode.AUTO
        self.padding = ft.padding.only(left=20, right=20, top=20)

        # --- Controles de la vista ---
        self.setup_controls()

        if self.app_state.user_profile:
            print("Perfil de usuario encontrado en app_state. Construyendo UI al instante.")
            self.build_ui(self.app_state.user_profile)
        else:
            print("Perfil no encontrado. Mostrando carga y buscando datos.")
            self.controls.append(get_loading_control(self.page, "Cargando perfil..."))
            self.page.run_task(self.load_profile_data)

    def setup_controls(self):
        """Inicializa los controles interactivos vacíos."""
        self.file_picker = ft.FilePicker(on_result=self.load_image)
        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(1920, 1, 1),
            last_date=datetime.datetime.now(),
            on_change=self.handle_date_selection_change,
        )
        self.page.overlay.extend([self.file_picker, self.date_picker])
        self.name_input = input_field('Nombre', '')
        self.email_input = input_field('Correo Electrónico', '', ft.KeyboardType.EMAIL)
        self.phone_input = input_field('Teléfono', '', ft.KeyboardType.PHONE)
        self.country_input = input_field('País', '')
        self.gender_input = selection_field('Género', GENDER)
        self.birthdate_input = input_field('Fecha de Nacimiento', '')

    def build_ui(self, data: dict):
        """Construye la interfaz de usuario completa con los datos del perfil."""
        self.update_fields(data)

        photo_b64 = data.get('photo_b64')
        if photo_b64:
            profile_image_content = ft.Image(src_base64=photo_b64, fit=ft.ImageFit.COVER, width=200, height=200, border_radius=100)
        else:
            profile_image_content = ft.Image(src='img/blank_user.png', fit=ft.ImageFit.COVER, width=200, height=200, border_radius=100)

        profile_photo = ft.Container(content=profile_image_content, alignment=ft.alignment.center)
        
        form_content = ft.Column([
            profile_photo,
            ft.Row([
                ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _: self.file_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE)),
                ft.IconButton(icon=ft.Icons.DELETE, on_click=self.delete_image)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            self.name_input, self.email_input, self.phone_input, self.country_input, self.gender_input,
            ft.Row([
                self.birthdate_input,
                ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=lambda _: self.page.open(self.date_picker))
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Row([
                ft.FilledButton(text='Actualizar', on_click=self.update_profile),
                ft.FilledButton(text='Cancelar', on_click=self.discard_changes)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ], scroll=ft.ScrollMode.AUTO, expand=True) # Hacemos que esta columna ocupe el espacio y tenga scroll

        content = ft.Column([
            ft.Row([ft.IconButton(icon=ft.Icons.LOGOUT, on_click=lambda _: self.page.go('/login'))], alignment=ft.MainAxisAlignment.END),
            logo,
            form_content, 
        ])

        self.controls.clear()
        self.controls.extend([
            ft.Container(content=content),
            nav_bar(self.page, 2),
        ])


    def update_fields(self, data: dict):
        """Rellena los campos del formulario con los datos proporcionados."""
        self.name_input.value = data.get('name', '')
        self.email_input.value = data.get('email', '')
        self.phone_input.value = data.get('phone', '')
        self.country_input.value = data.get('country', '')
        self.gender_input.value = data.get('gender', '')
        self.birthdate_input.value = data.get('birthdate', '')

    async def fetch_profile_data_async(self):
        """Simula la obtención de datos del perfil."""
        print("Obteniendo datos del perfil desde la API...")
        await asyncio.sleep(2)
        print("Datos obtenidos.")
        return DATA_EXAMPLE

    async def load_profile_data(self):
        """Carga los datos, los guarda en el estado y construye la UI."""
        data = await self.fetch_profile_data_async()
        self.app_state.user_profile = data
        try:
            self.build_ui(data)
            self.page.controls.clear()
            self.page.update()
        except Exception as e:
            print(f"Error al construir la UI: {e}")



    def update_profile(self, e):
        """Guarda los cambios del formulario en el estado central (app_state)."""
        updated_data = {
            "name": self.name_input.value,
            "email": self.email_input.value,
            "phone": self.phone_input.value,
            "country": self.country_input.value,
            "gender": self.gender_input.value,
            "birthdate": self.birthdate_input.value,
            # Mantenemos la foto si ya existía
            "photo_b64": self.app_state.user_profile.get('photo_b64')
        }
        self.app_state.user_profile = updated_data
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Perfil actualizado con éxito"), bgcolor=ft.colors.GREEN)
        self.page.snack_bar.open = True
        self.page.update()

    def discard_changes(self, e):
        """Descarta los cambios y recarga los datos originales desde el estado."""
        if self.app_state.user_profile:
            self.build_ui(self.app_state.user_profile)
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Cambios descartados"))
            self.page.snack_bar.open = True
            self.page.update()

    def load_image(self, e: ft.FilePickerResultEvent):
        """Actualiza la foto en el estado central y reconstruye la UI."""
        if not e.files: return
        with open(e.files[0].path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode("utf-8")
        if self.app_state.user_profile is None: self.app_state.user_profile = {}
        self.app_state.user_profile['photo_b64'] = img_base64
        self.build_ui(self.app_state.user_profile)
        self.page.update()

    def delete_image(self, e: ft.ControlEvent):
        """Restaura la imagen por defecto eliminándola del estado."""
        if self.app_state.user_profile and 'photo_b64' in self.app_state.user_profile:
            del self.app_state.user_profile['photo_b64']
            self.build_ui(self.app_state.user_profile)
            self.page.update()

    def handle_date_selection_change(self, e):
        """Actualiza el campo de fecha de nacimiento cuando se selecciona una fecha."""
        if self.date_picker.value:
            self.birthdate_input.value = f"{self.date_picker.value.strftime('%Y-%m-%d')}"
        else:
            self.birthdate_input.value = ""
        self.page.update()