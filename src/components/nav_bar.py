import flet as ft
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR


def nav_bar(page, selected_index=0):
    return ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icon(name=ft.Icons.LOCATION_ON_SHARP, color=PRIMARY_COLOR), label="Explorar"),
            ft.NavigationBarDestination(icon=ft.Icon(name=ft.Icons.SEARCH, color=PRIMARY_COLOR), label="Buscar"),
            ft.NavigationBarDestination(icon=ft.Icon(name=ft.Icons.SETTINGS, color=PRIMARY_COLOR), label="Ajustes"),
        ],
        selected_index=selected_index,
        indicator_color=SECONDARY_COLOR,
        on_change=lambda e: page.go(
            "/explore" if e.control.selected_index == 0 else
            "/search" if e.control.selected_index == 1 else
            "/user/index"
        )
        
    )

    


