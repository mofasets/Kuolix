import flet as ft
from components.logo import logo
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR,BACKGROUND_COLOR, PRIMARY_TEXT_COLOR
from components.input_field import input_field
from components.selection_field import selection_field
from sources.select_option import GENDER
import datetime


class SignupView(ft.View):
    """
    Clase que encapsula la vista de registro de nuevos usuarios,
    recopilando sus datos a través de un formulario.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # --- Propiedades de la vista ---
        self.route = "/signup"
        self.scroll = ft.ScrollMode.AUTO
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(10)

        # --- Controles de la vista ---
        self.setup_controls()
        self.setup_layout()

    def setup_controls(self):
        """Inicializa todos los controles interactivos de la vista."""
        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(1920, 1, 1),
            last_date=datetime.datetime.now(),
            on_change=self.handle_date_selection_change,
        )
        self.page.overlay.append(self.date_picker)
        
        # Campos del formulario
        self.name_input = input_field('Nombre', '')
        self.email_input = input_field('Correo Electrónico', '', ft.KeyboardType.EMAIL)
        self.phone_input = input_field('Teléfono', '', ft.KeyboardType.PHONE)
        self.country_input = input_field('País', '')
        self.gender_input = selection_field('Género', GENDER)
        self.birthdate_input = input_field('Fecha de Nacimiento', '')
        self.birthdate_input.read_only = True
        self.birthdate_input.expand = True
        self.password_input = input_field('Contraseña', '')
        self.password_input.password = True
        self.password_input.can_reveal_password = True

    def setup_layout(self):
        """Define la estructura y el layout de la vista."""
        login_link = ft.GestureDetector(
            content=ft.Text('Iniciar Sesión', color=PRIMARY_COLOR),
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=lambda _: self.page.go('/login'),
        )

        form_column = ft.Column([
            self.name_input,
            self.email_input,
            self.phone_input,
            self.country_input,
            self.gender_input,
            ft.Row([
                self.birthdate_input,
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    icon_color=PRIMARY_COLOR,
                    on_click=lambda _: self.page.open(self.date_picker),
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            self.password_input
        ], spacing=15)

        content_column = ft.Column([
            logo,
            ft.Text('Kuolix | Registrarse', size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            form_column,
            ft.Row([ft.Text('¿Ya tienes Cuenta?'), login_link], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=ft.ElevatedButton(
                    text='Registrarse',
                    bgcolor=PRIMARY_COLOR,
                    color=PRIMARY_TEXT_COLOR,
                    on_click=self.signup_user
                ),
                margin=ft.margin.only(top=20),
                border_radius=15,
            ),
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        signup_section = ft.Container(
            content=content_column,
            padding=ft.padding.all(20),
            alignment=ft.alignment.center,
            border_radius=15,
            width=400,
            shadow=ft.BoxShadow(
                spread_radius=1, blur_radius=1, color=ft.Colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0), blur_style=ft.ShadowBlurStyle.OUTER,
            ),
            margin=ft.margin.only(top=10, bottom=20),
        )

        self.controls = [signup_section]

    def handle_date_selection_change(self, e):
        """Actualiza el campo de fecha de nacimiento cuando se selecciona una fecha."""
        if self.date_picker.value:
            self.birthdate_input.value = f"{self.date_picker.value.strftime('%d/%m/%Y')}"
        else:
            self.birthdate_input.value = ""
        self.page.update()

    def signup_user(self, e):
        """
        Lógica para el registro de usuario. Por ahora, solo navega a /explore.
        Aquí iría la validación y guardado de datos.
        """
        # TODO: Añadir lógica de registro y validación de datos aquí
        print("Registrando nuevo usuario...")
        self.page.go('/explore')
