import flet as ft 
from sources.colors_pallete import PRIMARY_COLOR,SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from components.loading import get_loading_control 
from components.row_card import row_card
import base64
import time

message = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

def get_explore_view(page: ft.Page) -> ft.Column:
    page.controls.clear()

    def fetch_image_recognizer() -> ft.Container: 
        cards = ft.Column()
        for record in range(3):
            cards.controls.append(row_card('img/logo.png', 'Plant #1', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut'))
        image_response = ft.Container(
            content=ft.Column([
                ft.Text(message),
                cards
            ])
        )
        print('Get img recognizer...')
        time.sleep(2)
        print('Successfully...')
        return ft.Container(
            content=image_response,
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=100),
        )

    def load_image(e: ft.FilePickerResultEvent):
        img_base64, img_bytes = None, None
        auxImage = ft.Image(width=200, height=200, border_radius=20)
        if not e.files:
            text = ft.Text(DEFAULT_TEXT, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR)
            loaded_image.content = ft.Container(content=text, border=None)
            return "No file selected"
        
        with open(e.files[0].path, "rb") as f:
            img_bytes = f.read()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            auxImage.src_base64 = img_base64
            loaded_image.content = ft.Container(content=auxImage, padding=ft.padding.all(10), border_radius=20, bgcolor=PRIMARY_COLOR) 
        
        loading_control = get_loading_control(page, "Identificando ...")
        page.controls.append(loading_control)
        page.update()

        img_response = fetch_image_recognizer()
        if loading_control in page.controls:
            page.controls.remove(loading_control)

        if img_response:
            if explore_view in page.controls:
                page.controls.remove(explore_view)
            explore_view.controls.append(img_response)
            page.controls.append(explore_view)
            page.update()


    loaded_image = ft.Container(
        content=ft.Text(DEFAULT_TEXT, size=DEFAULT_TEXT_SIZE, color=DEFAULT_TEXT_COLOR),
        margin=ft.margin.only(top=20, bottom=20),
        border_radius=20,
        alignment=ft.alignment.center,
    )

    image_upload_floating_button = ft.FloatingActionButton(
        content=ft.Icon(name=ft.Icons.UPLOAD_FILE, color=SECONDARY_COLOR),
        bgcolor=PRIMARY_COLOR,
        on_click=lambda _: file_picker.pick_files(file_type=[ft.FilePickerFileType.IMAGE])
    )
    
    file_picker = ft.FilePicker(
        on_result=load_image
    )

    # Page Properties
    page.overlay.append(file_picker)
    page.floating_action_button = image_upload_floating_button


    explore_view = ft.Column(
        controls=[
            loaded_image,
        ] 
    )

    return explore_view

