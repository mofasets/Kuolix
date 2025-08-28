import os
import flet as ft
from views.login import LoginView
from views.signup import SignupView
from views.explore import ExploreView
from views.search import SearchView
from views.settings import SettingsView
from views.show import ShowView
from state import app_state
import httpx
from dotenv import load_dotenv
from sources.colors_pallete import BACKGROUND_COLOR

load_dotenv()
API_URL = os.getenv("API_BASE_URL")

def main(page: ft.Page):
    """
    Función principal que inicializa la aplicación, configura la página
    y maneja el enrutamiento entre las diferentes vistas.
    """

    app_state.api_client = httpx.AsyncClient(base_url=API_URL, timeout=10.0)

    def route_change(route):
        
        """
        Maneja el cambio de ruta, soportando rutas estáticas y dinámicas.
        """
        troute = ft.TemplateRoute(page.route)

        if troute.match("/login") or troute.match("/"):
            page.views.append(LoginView(page, app_state))
        if troute.match("/explore"):
            page.views.append(ExploreView(page, app_state))
        if troute.match("/search"):
            page.views.append(SearchView(page, app_state))
        if troute.match("/settings"):
            page.views.append(SettingsView(page, app_state))
            
        if troute.match("/show/:id"):
            item_id = troute.id
            page.views.append(ShowView(page, item_id=item_id, app_state=app_state))

        if troute.match("/signup"):
            page.views.append(SignupView(page, app_state))

        page.update()


    def view_pop(view):
        """
        Maneja el botón de "atrás" del navegador o del sistema operativo.
        """
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    # --- Configuración de la Página ---
    page.title = 'Kuolix: Plants Recognition'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = BACKGROUND_COLOR
    
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    async def cleanup(e):
        print("Cerrando la aplicación y el cliente de API...")
        await app_state.api_client.aclose()

    page.on_disconnect = cleanup
    page.go('/login')

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
