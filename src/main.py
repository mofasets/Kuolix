import flet as ft
import io
import base64

DEFAULT_TEXT_COLOR = "#202021"
PRIMARY_COLOR = "#663D8C"
BACKGROUND_COLOR = "#FAF9F6"
SECONDARY_COLOR = "#F3E2F4"
DEFAULT_TEXT = """
Agrega una foto de la planta que deseas identificar, y te indicaré si es medicinal o no, y sus propiedades. Tan solo debes darle “clic” al botón de abajo a la derecha.
"""
DEFAULT_TEXT_SIZE = 16

def main(page: ft.Page):
    # Funtions
    def show_logo():
        logo = ft.Image(src='img/logo.png', width=100, height=100)
        app_name = ft.Text("Kuolix", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR)
        return ft.ResponsiveRow(
            controls=[ft.Container(
                content=ft.Row([logo, app_name], 
                alignment=ft.MainAxisAlignment.CENTER),
                margin=ft.margin.only(top=40),
            )],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def load_image(e: ft.FilePickerResultEvent):
        img_base64, img_bytes = None, None
        auxImage = ft.Image(width=200, height=200, border_radius=20)
        if e.files:
            with open(e.files[0].path, "rb") as f:
                img_bytes = f.read()
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                auxImage.src_base64 = img_base64
                loaded_image.content = ft.Container(content=auxImage, padding=ft.padding.all(10), border_radius=20, bgcolor=PRIMARY_COLOR) 
                page.add(loading_layout)
        else:
            text = ft.Text(DEFAULT_TEXT, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR)
            loaded_image.content = ft.Container(content=text, border=None)
        page.update()
        

    # Controls
    loaded_image = ft.Container(
        content=ft.Text(DEFAULT_TEXT, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR),
        margin=ft.margin.only(top=20),
        border_radius=20,
        alignment=ft.alignment.center,
    )

    file_picker = ft.FilePicker(
        on_result=load_image
    )

    navBar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icon(name=ft.Icons.LOCATION_ON_SHARP, color=PRIMARY_COLOR), label="Explorar"),
            ft.NavigationBarDestination(icon=ft.Icon(name=ft.Icons.SEARCH, color=PRIMARY_COLOR), label="Buscar"),
        ],
        selected_index=0,
        indicator_color=SECONDARY_COLOR
    )

    floating_action_button = ft.FloatingActionButton(
        content=ft.Icon(name=ft.Icons.IMAGE_SEARCH, color=ft.Colors.WHITE),
        bgcolor=PRIMARY_COLOR,
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["png", "jpg", "jpeg"])
    )

    logo = show_logo()

    loading_spinner = ft.ProgressRing(color=PRIMARY_COLOR, width=40, height=40)


    layout_image_recognition = ft.Column([
        logo,
        loaded_image,
    ], alignment=ft.MainAxisAlignment.CENTER)

    loading_layout = ft.Container(
        content=ft.Column([
            loading_spinner,
            ft.Text("Cargando...", size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR),
        ]), alignment=ft.alignment.center
    ) 

    # Page configuration
    page.bgcolor = BACKGROUND_COLOR
    page.title = 'Kuolix: Plants Recognition'
    page.window_width = 1000
    page.window_max_width = 400
    page.window_height = 100
    page.theme_mode = ft.ThemeMode.LIGHT
    page.overlay.append(file_picker)
    page.floating_action_button = floating_action_button
    page.add(
        navBar,
        layout_image_recognition,
    )
ft.app(main)
