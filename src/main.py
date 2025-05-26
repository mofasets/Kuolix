import flet as ft
import google.generativeai as genai
from PIL import Image
import io
import io
import base64
from prompt_base import PROMPT
from sources.colors_pallete import BACKGROUND_COLOR, SECONDARY_COLOR, PRIMARY_COLOR
from views.explore import get_explore_view

def main(page: ft.Page):
    #Functions
    def on_navigation_change(e):
        if e.control.selected_index == 0:
            page.controls = [explore_view]
        elif e.control.selected_index == 1:
            page.controls.clear()
        elif e.control.selected_index == 2:
            page.controls.clear()

        page.controls.append(nav_bar)
        page.update()

    # Navigation Bar
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icon(name=ft.Icons.LOCATION_ON_SHARP, color=PRIMARY_COLOR), label="Explorar"),
            ft.NavigationBarDestination(icon=ft.Icon(name=ft.Icons.SEARCH, color=PRIMARY_COLOR), label="Buscar"),
            ft.NavigationBarDestination(icon=ft.Icon(name=ft.Icons.SETTINGS, color=PRIMARY_COLOR), label="Ajustes"),
        ],
        selected_index=0,
        indicator_color=SECONDARY_COLOR,
        on_change=on_navigation_change
    )



    # Page configuration
    page.bgcolor = BACKGROUND_COLOR
    page.title = 'Kuolix: Plants Recognition'
    page.window_width = 1000
    page.window_max_width = 400
    page.window_height = 100
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    

    #Views
    explore_view = get_explore_view(page)
    page.add(
        explore_view,
        nav_bar
    )
ft.app(main)
