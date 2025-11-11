import flet as ft
import httpx
from sources.colors_pallete import (
    PRIMARY_COLOR, 
    SECONDARY_COLOR, 
    DEFAULT_TEXT_SEARCH, 
    DEFAULT_TEXT_SIZE, 
    DEFAULT_TEXT_COLOR
)
from components.loading import get_loading_control
from components.row_card import row_card
from components.logo import logo
from components.nav_bar import nav_bar
from state import AppState
from typing import List, Set

class SearchView(ft.View):
    """
    Una clase que encapsula la vista de búsqueda, permitiendo al usuario
    ingresar texto y ver una lista de resultados de forma asíncrona.
    """
    def __init__(self, page: ft.Page, app_state: AppState):
        super().__init__()

        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.padding = ft.padding.all(0)
        self.response_container = None
        self.app_state = app_state
        self.route = "/search"
        self.filter_toggle = None
        self.current_filter_mode = "recommendations"
        self.page.controls = [ft.Container(content=get_loading_control(self.page, "Cargando..."), expand=True)]
        
        if not self.app_state.search_results:
            self.page.run_task(self.load_initial_recommendations)
        else:
            self.build_ui()

    def build_ui(self):
        """
        Construye la interfaz de usuario completa basándose en el estado actual.
        """
        self.search_input = ft.TextField(
            label="Buscar", value=self.app_state.search_query, 
            border_radius=15, border_color=PRIMARY_COLOR,
            border_width=2, expand=True, on_submit=self.search_action
        )

        self.icon_button = ft.IconButton(
            icon=ft.Icons.SEARCH, icon_size=30, bgcolor=SECONDARY_COLOR, 
            icon_color=PRIMARY_COLOR, on_click=self.search_action
        )

        self.filter_toggle = ft.SegmentedButton(

            # Por defecto, seleccionamos "recommendations"
            selected={self.current_filter_mode},
            on_change=self.on_filter_change,
            expand=True,
            style=ft.ButtonStyle(color=PRIMARY_COLOR, icon_color=PRIMARY_COLOR, bgcolor={ft.ControlState.SELECTED: SECONDARY_COLOR}),
            segments=[
                ft.Segment(value="all", label=ft.Text("Todo")),
                ft.Segment(value="recommendations", label=ft.Text("Para Ti")),
                ft.Segment(value="non_verified", label=ft.Text("Sin verificar")),
            ]
        )

        # Floating Action Button.
        self.floating_action_button = ft.FloatingActionButton(
            content=ft.Icon(name=ft.Icons.EDIT_NOTE, color=SECONDARY_COLOR),
            bgcolor=PRIMARY_COLOR,
            on_click=lambda _:self.page.go('/create')
        )
        
        self.results_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        if self.app_state.search_results:
            for res in self.app_state.search_results:
                self.results_container.controls.append(
                    row_card(self.page, res, back_route="/search")
                )
        else:
            self.results_container.controls.append(
                ft.Container(
                    content=ft.Text(DEFAULT_TEXT_SEARCH, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                    margin=ft.margin.only(top=50), alignment=ft.alignment.center
                )
            )

        self.controls.clear()
        self.controls = [
            ft.Container(content=ft.Column([
                logo,
                ft.Row([self.search_input, self.icon_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=5),
                ft.Row([self.filter_toggle],alignment=ft.MainAxisAlignment.CENTER,spacing=5),
                ft.Container(content=self.results_container, expand=True, margin=ft.margin.only(top=30, bottom=100)),
            ]),
                padding=ft.padding.only(left=15, right=15)
            ),
            nav_bar(self.page, 1)
        ]

    async def on_filter_change(self, e: ft.ControlEvent):
        """Se activa al cambiar entre 'Recomendaciones' y 'All'."""
        mode = e.data
        if "recommendations" in mode:
            self.search_input.value = ""
            self.app_state.search_query = ""
            await self.load_initial_recommendations()
        elif "all" in mode:
            self.search_input.value = ""
            self.app_state.search_query = ""
            await self.search_all()
        elif "non_verified" in mode:
            self.search_input.value = ""
            self.app_state.search_query = ""
            await self.search_all_non_verified()

    async def fetch_search_results_async(self, query: str) -> list[dict]:
        """
        Simula una llamada a API asíncrona para obtener resultados de búsqueda.
        """
        print(f'Buscando resultados en la API para: {query}...')
    
        token = self.app_state.token
        if not token:
            self.page.go("/login")
            return []

        headers = {"Authorization": f"Bearer {token}"}        
        try:
        
            response = await self.app_state.api_client.get(
                f"/search/search_query/{query}", 
                headers=headers
            )
        
            response.raise_for_status()

            results_data = response.json()
            print(f"Éxito. Se encontraron {len(results_data)} resultados.")
            return results_data

        except httpx.HTTPStatusError as exc:
            print(f"Error de API: {exc.response.status_code} - {exc.response.text}")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la búsqueda: {e}")
        return []

    async def load_initial_recommendations(self):
        """
        Tarea asíncrona que llama a la API para obtener recomendaciones,
        las guarda en el estado y luego construye la UI.
        """
        if self.filter_toggle:
            self.filter_toggle.selected = {"recommendations"}

        recommendations = await self.fetch_recommendations()
        self.app_state.search_results = recommendations
        
        self.build_ui()
        self.page.update()

    async def search_all(self):
        self.results_container.controls.clear()
        self.results_container.controls.append(get_loading_control(self.page, "Buscando..."))
        self.page.update()

        results = await self.fetch_all()
        self.app_state.search_results = results
        
        self.results_container.controls.clear()
        if self.app_state.search_results:
            for res in self.app_state.search_results:
                self.results_container.controls.append(
                    row_card(self.page, res, back_route="/search")
                )
        self.page.update()

    def search_action(self, e):
        """
        Activador síncrono: guarda el término de búsqueda y lanza la tarea asíncrona.
        """
        # if self.filter_toggle:
        #     self.filter_toggle.selected = {"all"}

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
        self.results_container.controls.clear()
        self.results_container.controls.append(get_loading_control(self.page, "Buscando..."))
        self.page.update()

        results = await self.fetch_search_results_async(self.app_state.search_query)
        self.app_state.search_results = results
        
        self.results_container.controls.clear()
        if self.app_state.search_results:
            for res in self.app_state.search_results:
                self.results_container.controls.append(
                    row_card(self.page, res, back_route="/search")
                )
        else:
             self.results_container.controls.append(
                ft.Container(
                    content=ft.Text("No se encontraron resultados.", size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                    margin=ft.margin.only(top=50), alignment=ft.alignment.center
                )
            )
        self.page.update()

    async def fetch_recommendations(self) -> List[dict]:
        """"""
        user_id = self.app_state.current_user.get('id') if self.app_state.current_user else None
        token = self.app_state.token
        if not token:
            self.page.go("/login")
            return []

        headers = {"Authorization": f"Bearer {token}"}        
        try:
        
            response = await self.app_state.api_client.get(
                f"/search/index/{user_id}", 
                headers=headers
            )
        
            response.raise_for_status()

            results_data = response.json()
            print(f"Éxito. Se encontraron {len(results_data)} resultados.")
            return results_data

        except httpx.HTTPStatusError as exc:
            print(f"Error de API: {exc.response.status_code} - {exc.response.text}")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la búsqueda: {e}")
        return []

    async def fetch_all(self) -> List[dict]:
        """Get the full lists of plants"""

        token = self.app_state.token
        if not token:
            self.page.go("/login")
            return []

        headers = {"Authorization": f"Bearer {token}"}        
        try:
        
            response = await self.app_state.api_client.get(
                f"/search/all", 
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

    async def search_all_non_verified(self) -> List[dict]:
        self.results_container.controls.clear()
        self.results_container.controls.append(get_loading_control(self.page, "Buscando..."))
        self.page.update()

        results = await self.fetch_all_non_verified()
        self.app_state.search_results = results
        
        self.results_container.controls.clear()
        if self.app_state.search_results:
            for res in self.app_state.search_results:
                self.results_container.controls.append(
                    row_card(self.page, res, back_route="/search")
                )
        self.page.update()

    async def fetch_all_non_verified(self) -> List[dict]:
        """Get the full lists of plants"""

        token = self.app_state.token
        if not token:
            self.page.go("/login")
            return []

        headers = {"Authorization": f"Bearer {token}"}        
        try:
        
            response = await self.app_state.api_client.get(
                f"/search/all_non_verified", 
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
