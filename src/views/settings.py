import flet as ft
import time
import base64
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR, DEFAULT_TEXT, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR, PRIMARY_TEXT_COLOR, SECONDARY_TEXT_COLOR
from sources.select_option import GENDER
from components.input_field import input_field
from components.selection_field import selection_field
from components.loading import get_loading_control
import datetime
from components.logo import logo
from components.nav_bar import nav_bar

# ELIMINAR CUANDO SE INTEGRE CON EL BACKEND
DATA_EXAMPLE = {
    "name": "Sebastian Osto",
    "email": "sebastianosto1@gmail.com",
    "phone": "04241234567",
    "country": "Venezuela",
    "gender": "Masculino",
    "birthdate": "1990-01-01"
}

def get_settings_view(page: ft.Page) -> ft.View:
    
    def store_data(data: dict[str: str]):
        data['name'] = name_input.value
        data['email'] = email_input.value
        data['phone'] = phone_input.value
        data['country'] = country_input.value
        data['gender'] = gender_input.value
        data['birthdate'] = birthdate_input.value

    def update_fields(data: dict[str: str]):
        nonlocal name_input, email_input, phone_input, country_input, gender_input, birthdate_input
        name_input.value = data.get('name', '')
        email_input.value = data.get('email', '')
        phone_input.value = data.get('phone', '')
        country_input.value = data.get('country', '')
        gender_input.value = data.get('gender','')
        birthdate_input.value = data.get('birthdate','')

    def fetch_profile_data():
        # Simulate fetching profile data
        time.sleep(1)
        return DATA_EXAMPLE
        
    def load_profile_data():
        loading_control = get_loading_control(page, "Cargando datos del perfil ...")
        page.views.clear()
        page.views.append(ft.View(controls=[loading_control]))
                          
        page.update()
        response = fetch_profile_data()
        
        if loading_control in page.controls:
            page.controls.remove(loading_control)

        return response

    def load_image(e: ft.FilePickerResultEvent):
        img_base64, img_bytes = None, None
        auxImage = ft.Image(width=200, height=200, border_radius=100, fit=ft.ImageFit.COVER)
        
        with open(e.files[0].path, "rb") as f:
            img_bytes = f.read()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            auxImage.src_base64 = img_base64
            profile_photo.content = ft.Container(content=auxImage) 
        page.update()

    def delete_image(e: ft.ControlEvent):
        profile_photo.content = ft.Image(
            src='img/blank_user.png',
            fit=ft.ImageFit.COVER,
            width=200,
            height=200,
            border_radius=100,
        )
        page.update()

    def handle_date_selection_change(e):
        if date_picker.value:
            birthdate_input.value = f"{date_picker.value.strftime('%d/%m/%Y')}"
        else:
            birthdate_input.value = "Ninguna"
        page.update()

    def handle_date_picker_dismiss(e):
        page.update()

    def update_profile(e):
        if settings_view in page.controls:
            page.controls.remove(settings_view)
            page.update()
        store_data(DATA_EXAMPLE)
        response = load_profile_data()
        if response:
            update_fields(response)
        page.controls.append(form)
        page.update()

    def discard_changes(e):
        if settings_view in page.controls:
            page.controls.remove(settings_view)
            page.update()
        response = load_profile_data()
        if response:
            update_fields(response)
        page.controls.append(form)
        page.update()

    # Controls
    date_picker = ft.DatePicker(
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime(2030, 12, 31),
        value=datetime.datetime.now(),
        date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR,
        on_change=handle_date_selection_change,
        on_dismiss=handle_date_picker_dismiss,
        cancel_text="Cancelar",
        confirm_text="Aceptar",
        help_text="Selecciona una fecha"
    )

    file_picker = ft.FilePicker(
        on_result=load_image
    )

    logout_button = ft.IconButton(
        icon=ft.Icons.LOGOUT,
        tooltip='Cerrar Sesión',
        icon_color=PRIMARY_TEXT_COLOR,
        icon_size=20,
        bgcolor=PRIMARY_COLOR,
        on_click=lambda _: page.go('/login')
    )


    open_date_picker_button = ft.IconButton(
        icon_size=20,
        bgcolor=SECONDARY_COLOR,
        icon_color=PRIMARY_COLOR,
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: page.open(date_picker), # Usa .pick_date() para mostrarlo
    )

    update_button = ft.FilledButton(
        text='Actualizar',
        color=PRIMARY_TEXT_COLOR,
        bgcolor=PRIMARY_COLOR,
        on_click=update_profile
    )

    cancel_button = ft.FilledButton(
        text='Cancelar',
        color=SECONDARY_TEXT_COLOR,
        bgcolor=SECONDARY_COLOR,
        on_click=discard_changes
    )

    edit_profile_photo_button = ft.IconButton(
        icon=ft.Icons.EDIT,
        tooltip='Editar Foto de Perfil',
        icon_color=PRIMARY_TEXT_COLOR,
        icon_size=20,
        bgcolor=PRIMARY_COLOR,
        on_click=lambda _: file_picker.pick_files(file_type=[ft.FilePickerFileType.IMAGE])
    )

    delete_default_photo_button = ft.IconButton(
        icon=ft.Icons.DELETE,
        tooltip='Eliminar Foto de Perfil',
        icon_color=PRIMARY_TEXT_COLOR,
        icon_size=20,
        bgcolor=PRIMARY_COLOR,
        on_click=delete_image
    )

    profile_photo = ft.Container(
        content=ft.Image(
            src='img/blank_user.png',
            fit=ft.ImageFit.COVER,
            width=200,
            height=200,
            border_radius=100,
        ),
        alignment=ft.alignment.center,
    )


    name_input = input_field('Nombre', value='')
    email_input = input_field('Correo Electrónico', input_type=ft.KeyboardType.EMAIL, value='')
    phone_input = input_field('Teléfono', input_type=ft.KeyboardType.PHONE, value='')
    country_input = input_field('País', value='')
    gender_input = selection_field('Género', GENDER)
    birthdate_input = input_field('Fecha de Nacimiento', value='')
    birthdate_input.read_only = True 
    birthdate_input.expand = True

    content = ft.Column([
        profile_photo,
        ft.Row([
            edit_profile_photo_button,
            delete_default_photo_button
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        name_input,
        email_input,
        phone_input,
        country_input,
        gender_input,
        ft.Row([
            birthdate_input, 
            open_date_picker_button
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        ft.Row([
            update_button,
            cancel_button
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    ], 
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )


    form = ft.Container(
        content=content,
        alignment=ft.alignment.center,
        expand=True,
    )

    nav = nav_bar(page, 2)

    response = load_profile_data()
    if response:
        update_fields(response)


    settings_view = ft.View(
        controls=[
            ft.Row([logout_button], alignment=ft.MainAxisAlignment.END),
            logo,
            form,
            nav
        ],
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.only(left=20, right=20, top=20)
    )

    page.overlay.append(file_picker)
    page.overlay.append(date_picker)
    

    return settings_view