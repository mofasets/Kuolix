import flet as ft 
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from views.layout import logo
import base64


def get_explore_view(page: ft.Page) -> ft.Column:

    def load_image(e: ft.FilePickerResultEvent):
        img_base64, img_bytes = None, None
        auxImage = ft.Image(width=200, height=200, border_radius=20)
        if e.files:
            with open(e.files[0].path, "rb") as f:
                img_bytes = f.read()
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                auxImage.src_base64 = img_base64
                loaded_image.content = ft.Container(content=auxImage, padding=ft.padding.all(10), border_radius=20, bgcolor=PRIMARY_COLOR) 
        else:
            text = ft.Text(DEFAULT_TEXT, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR)
            loaded_image.content = ft.Container(content=text, border=None)
        page.update()

    loaded_image = ft.Container(
        content=ft.Text(DEFAULT_TEXT, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR),
        margin=ft.margin.only(top=20),
        border_radius=20,
        alignment=ft.alignment.center,
    )

    floating_action_button = ft.FloatingActionButton(
        content=ft.Icon(name=ft.Icons.IMAGE_SEARCH, color=ft.Colors.WHITE),
        bgcolor=PRIMARY_COLOR,
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["png", "jpg", "jpeg"])
    )

    file_picker = ft.FilePicker(
        on_result=load_image
    )

    # Add the file picker to the page
    page.floating_action_button = floating_action_button
    page.overlay.append(file_picker)

    explore_view = ft.Column(
        controls=[
            logo,
            loaded_image
        ],
            alignment=ft.MainAxisAlignment.CENTER
    )

    return explore_view

