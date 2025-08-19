import flet as ft
import io
import base64
from prompt_base import PROMPT
from sources.colors_pallete import BACKGROUND_COLOR, SECONDARY_COLOR, PRIMARY_COLOR
from views.explore import get_explore_view
from views.search import get_search_view
from views.show import get_show_view
from views.settings import get_settings_view
from views.login import get_login_view
from views.signup import get_signup_view
import time

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()

        if page.route == "/explore":
            page.views.append(get_explore_view(page))
        elif page.route == "/search":
            page.views.append(get_search_view(page))
        elif page.route == "/settings":
            page.views.append(get_settings_view(page))
        elif page.route == "/login":
            page.views.append(get_login_view(page))
        elif page.route == "/signup":
            page.views.append(get_signup_view(page))
        elif page.route == "/show":
            page.views.append(get_show_view(page))

        page.update()

    # def view_pop(view):
    #     print(page.views)
    #     if page.views:
    #         page.views.pop()
    #         top_view = page.views[-1]
    #         page.go(top_view.route)
    #     else:
    #         page.go('/explore')

    # Page configuration
    page.bgcolor = BACKGROUND_COLOR
    page.title = 'Kuolix: Plants Recognition'
    page.window_width = 1000
    page.window_max_width = 400
    page.window_height = 100
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.on_route_change = route_change
    # page.on_view_pop = view_pop

    #Views
    page.go('/login')
ft.app(main)
