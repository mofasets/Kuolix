import flet as ft
from components.logo import logo
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR,BACKGROUND_COLOR, PRIMARY_TEXT_COLOR

class LoginView(ft.View):
    """
    Clase que encapsula la vista de inicio de sesión, manejando la entrada
    del usuario y la navegación a otras vistas como registro o la principal.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # --- Propiedades de la vista ---
        self.route = "/login"
        self.scroll = ft.ScrollMode.AUTO
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(10)

        # --- Controles de la vista ---
        
        self.email_input = ft.TextField(
            label='Correo',
            keyboard_type=ft.KeyboardType.EMAIL,
            border_radius=15,
            border_color='#D3D3D3',
            focused_border_color=PRIMARY_COLOR,
            border_width=1,
            label_style=ft.TextStyle(color=PRIMARY_COLOR)
        )

        self.password_input = ft.TextField(
            label='Contraseña',
            password=True,
            can_reveal_password=True,
            border_radius=15,
            border_color='#D3D3D3',
            focused_border_color=PRIMARY_COLOR,
            border_width=1,
            label_style=ft.TextStyle(color=PRIMARY_COLOR),
            on_submit=self.login # Permite iniciar sesión con "Enter"
        )

        signup_link = ft.GestureDetector(
            content=ft.Text('Regístrate', color=PRIMARY_COLOR),
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=self.go_to_signup,
        )

        login_button = ft.Container(
            content=ft.ElevatedButton(
                text='Iniciar Sesión',
                bgcolor=PRIMARY_COLOR,
                color=PRIMARY_TEXT_COLOR,
                on_click=self.login
            ),
            margin=ft.margin.only(top=30),
            border_radius=15,
        )

        # --- Layout de la vista ---
        
        content_column = ft.Column([
            logo,
            ft.Text(
                'Kuolix | Inicio de Sesión',
                size=16,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            self.email_input,
            self.password_input,
            ft.Row([ft.Text('¿No tienes Cuenta?'), signup_link], alignment=ft.MainAxisAlignment.CENTER),
            login_button,
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        login_section = ft.Container(
            content=content_column,
            padding=ft.padding.all(20),
            alignment=ft.alignment.center,
            border_radius=15,
            width=400,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=1,
                color=ft.Colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
            margin=ft.margin.only(top=50),
        )

        self.controls = [login_section]

    def login(self, e):
        """
        Lógica para el inicio de sesión. Por ahora, solo navega a /explore.
        Aquí iría la validación de email/contraseña.
        """
        # TODO: Añadir lógica de autenticación aquí
        print(f"Email: {self.email_input.value}, Contraseña: {self.password_input.value}")
        self.page.go('/explore')

    def go_to_signup(self, e):
        """Navega a la página de registro."""
        self.page.go('/signup')
