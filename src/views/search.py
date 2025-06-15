import flet as ft
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SEARCH, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from components.loading import get_loading_control
import time
from components.row_card import row_card

def get_search_view(page: ft.Page) -> ft.Column:

    def fetch_image_recognizer() -> ft.Container: 
        cards = ft.Column()
        for record in range(10):
            cards.controls.append(row_card('img/logo.png', 'Plant #1', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut'))
        image_response = ft.Container(
            content=ft.Column([
                cards
            ],
                expand=True,
            )
        )
        print('Get img recognizer...')
        time.sleep(2)
        print('Successfully...')
        return ft.Container(
            content=image_response,
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=30, bottom=100),
        )

    def search_action(e):
        nonlocal search_view, search_input, initial_text, icon_button, content, img_response
        if search_input.value.strip() != "":

            if img_response is not None and img_response in content.controls:
                content.controls.remove(img_response)

            if initial_text in content.controls:
                content.controls.remove(initial_text)
            loading_control = get_loading_control(page, "Buscando ...")
            content.controls.append(loading_control)
            page.update()

            img_response = fetch_image_recognizer()
            if img_response:
                if loading_control in content.controls:
                    content.controls.remove(loading_control)
                content.controls.append(img_response)
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

    img_response = None
    
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


    search_view = ft.Container(
        content=content,
        expand=True,
        alignment=ft.alignment.center,
        padding=ft.padding.only(left=10, right=10),
    )

    return search_view