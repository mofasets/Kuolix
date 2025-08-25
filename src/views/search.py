import flet as ft
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SEARCH, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from components.loading import get_loading_control
import time
from components.row_card import row_card
from views.show import ShowView
from components.logo import logo
from components.nav_bar import nav_bar
import asyncio
from state import AppState

class SearchView(ft.View):
    """
    Una clase que encapsula la vista de búsqueda, permitiendo al usuario
    ingresar texto y ver una lista de resultados de forma asíncrona.
    """
    def __init__(self, page: ft.Page, app_state: AppState):
        super().__init__()

        self.page = page
       
        self.scroll = ft.ScrollMode.AUTO
        self.padding = ft.padding.only(left=20, right=20)
        self.response_container = None
        self.app_state = app_state
        self.route = "/search"

        self.build_ui()

    def build_ui(self):
        """
        Construye la interfaz de usuario completa basándose en el estado actual.
        """
        self.search_input = ft.TextField(
            label="Buscar",
            value=self.app_state.search_query, 
            border_radius=15,
            border_color=PRIMARY_COLOR,
            border_width=2,
            expand=True,
            on_submit=self.search_action
        )

        self.icon_button = ft.IconButton(
            icon=ft.Icons.SEARCH, 
            icon_size=30, 
            bgcolor=SECONDARY_COLOR, 
            icon_color=PRIMARY_COLOR,
            on_click=self.search_action
        )
        
        if self.app_state.search_results:
            results_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
            for res in self.app_state.search_results:
                results_column.controls.append(
                    row_card(self.page, res['id'], res['img'], res['title'], res['desc'], back_route="/search")
                )
            main_content = ft.Container(content=results_column, expand=True, margin=ft.margin.only(top=30, bottom=100))
        else:
            main_content = ft.Container(
                content=ft.Text(DEFAULT_TEXT_SEARCH, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                margin=ft.margin.only(top=50),
                alignment=ft.alignment.center
            )

        self.content_column = ft.Container(
            content=ft.Column([
                ft.Row([self.search_input, self.icon_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
                main_content
            ]),
            expand=True,
            padding=ft.padding.only(left=20, right=20)
        )

        self.controls = [logo, self.content_column, nav_bar(self.page, 1)]

    async def fetch_search_results_async(self, query: str) -> list[dict]:
        """
        Simula una llamada a API asíncrona para obtener resultados de búsqueda.
        """
        print(f'Buscando resultados para: {query}...')
        await asyncio.sleep(2)
        print('Éxito.')
        
        results_data = []
        for i in range(10):
            results_data.append({
                "id": f"planta_{i+1}", 
                "img": "img/logo.png", 
                "title": f"Planta #{i+1} (Resultado)", 
                "desc": "Lorem ipsum dolor sit amet..."
            })
        return results_data

    def search_action(self, e):
        """
        Activador síncrono: guarda el término de búsqueda y lanza la tarea asíncrona.
        """
        term = self.search_input.value.strip()
        if not term:
            return
        
        # Guardamos el término de búsqueda en el estado central.
        self.app_state.search_query = term
        
        # Lanzamos la tarea de búsqueda real en segundo plano.
        self.page.run_task(self.search_async)
    
    async def search_async(self):
        """
        Trabajador asíncrono: muestra la carga, busca, guarda resultados y reconstruye la UI.
        """
        loading = get_loading_control(self.page, "Buscando...")
        self.content_column.content.controls.pop()
        self.content_column.content.controls.append(loading)
        self.page.update()

        await asyncio.sleep(0.01)

        results = await self.fetch_search_results_async(self.app_state.search_query)

        self.app_state.search_results = results
        
        self.build_ui()
        self.page.update()
