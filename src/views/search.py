import flet as ft
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SEARCH, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from components.loading import get_loading_control
import time
from components.row_card import row_card
from views.show import get_show_view
from components.logo import logo
from components.nav_bar import nav_bar
import asyncio




def get_search_view(page: ft.Page) -> ft.View:

    async def fetch_image_recognizer() -> ft.Container: 
        cards = ft.Column()
        for record in range(10):
            cards.controls.append(row_card(search_view, page, 'img/logo.png', 'Plant #1', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut'*30))
        image_response = ft.Container(
            content=ft.Column([
                cards
            ],
                expand=True,
            )
        )
        print('Get img recognizer...')
        await asyncio.sleep(2)
        print('Successfully...')
        return ft.Container(
            content=image_response,
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=30, bottom=100, left=10, right=10),
        )

    async def search_action(e):
        nonlocal search_view, search_input, initial_text, icon_button, content, response
        if search_input.value.strip() != "":

            if response is not None and response in content.controls:
                content.controls.remove(response)

            if initial_text in content.controls:
                content.controls.remove(initial_text)
            loading_control = get_loading_control(page, "Buscando ...")
            content.controls.append(loading_control)
            page.update()

            response = await fetch_image_recognizer()
            if response:
                if loading_control in content.controls:
                    content.controls.remove(loading_control)
                content.controls.append(response)
                page.update()

    initial_text = ft.Container(
        content=ft.Text(
            DEFAULT_TEXT_SEARCH,
            size=DEFAULT_TEXT_SIZE,
            color=DEFAULT_TEXT_COLOR,
            text_align=ft.TextAlign.CENTER,
        ),
        margin=ft.margin.only(top=50),
        alignment=ft.alignment.center,
    )

    response = None
    
    search_input = ft.TextField(
        label="Buscar",
        border_radius=15,
        border_color=PRIMARY_COLOR,
        border_width=2,
        expand=True,
    )

    icon_button = ft.IconButton(
        icon=ft.Icons.SEARCH, 
        icon_size=30, 
        bgcolor=SECONDARY_COLOR, 
        icon_color=PRIMARY_COLOR,
        on_click=search_action,
    )
    
    content= ft.Column([
        ft.Row([
            search_input,
            icon_button
        ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
        ),
        initial_text
    ])

    nav = nav_bar(page)

    search_view = ft.View(
        controls=[
            logo,
            content,
            nav
        ],
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.only(left=20, right=20),
    )

    return search_view