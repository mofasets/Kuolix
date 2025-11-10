import flet as ft
from components.logo import logo
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR,BACKGROUND_COLOR, PRIMARY_TEXT_COLOR
from state import AppState
import httpx

class LoginView(ft.View):
    """
    Clase que encapsula la vista de inicio de sesión, manejando la entrada
    del usuario y la navegación a otras vistas como registro o la principal.
    """
    def __init__(self, page: ft.Page, app_state: AppState):
        super().__init__()
        self.page = page
        self.app_state = app_state
        self.route = "/login"
        self.scroll = ft.ScrollMode.AUTO
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(10)
        self.error_text = ft.Text(value="", color=ft.Colors.RED, visible=False)
        self.error_text.visible = False

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

        self.login_button_control = ft.ElevatedButton(
            text='Iniciar Sesión',
            bgcolor=PRIMARY_COLOR,
            color=PRIMARY_TEXT_COLOR,
            on_click=self.login
        )
        login_button = ft.Container(
            content=self.login_button_control,
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
            self.error_text
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        login_section = ft.Container(
            content=content_column,
            padding=ft.padding.all(20),
            alignment=ft.alignment.center,
            width=400,
            margin=ft.margin.only(top=50),
        )
        self.controls = [login_section]

    async def login(self, e):
        """
        Lógica para el inicio de sesión. Por ahora, solo navega a /explore.
        Aquí iría la validación de email/contraseña.
        """
        self.error_text.visible = False
        self.login_button_control.disabled = True
        self.page.update()

        try:
            email = self.email_input.value
            password = self.password_input.value

            if not email or not password:
                raise ValueError("El correo y la contraseña no pueden estar vacíos.")
            
            login_data = {"username": email, "password": password}
            
            print("Intentando iniciar sesión...")
            response = await self.app_state.api_client.post("/auth/token", data=login_data)
            response.raise_for_status() 
            
            data = response.json()
            access_token = data.get("access_token")

            if not access_token:
                raise ValueError("La respuesta de la API no contiene un token de acceso.")
            self.app_state.token = access_token

            # Second call to API  process
            headers = {"Authorization": f"Bearer {access_token}"}
            user_profile_response = await self.app_state.api_client.get("/auth/me", headers=headers)
            user_profile_response.raise_for_status()
            
            user_data = user_profile_response.json()
            
            self.app_state.current_user = user_data
            self.page.go('/explore')

        except httpx.HTTPStatusError as exc:
            print(f"Error de API: {exc}")
            self.error_text.value = "Correo o contraseña incorrectos."
            self.error_text.visible = True
        except (httpx.ConnectError, httpx.TimeoutException):
            print("Error de conexión con el servidor.")
            self.error_text.value = "No se pudo conectar al servidor. Inténtalo más tarde."
            self.error_text.visible = True
        except Exception as exc:
            print(f"Ocurrió un error inesperado: {exc}")
            self.error_text.value = str(exc)
            self.error_text.visible = True
        
        finally:
            self.login_button_control.disabled = False
            self.page.update()
        
    def go_to_signup(self, e):
        """Navega a la página de registro."""
        self.page.go('/signup')
