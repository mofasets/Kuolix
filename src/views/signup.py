import flet as ft
from components.logo import logo
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR,BACKGROUND_COLOR, PRIMARY_TEXT_COLOR
from components.input_field import input_field
from components.selection_field import selection_field
from sources.select_option import GENDER
import datetime


def get_signup_view(page: ft.Page) -> ft.View:

    def handle_date_selection_change(e):
        if date_picker.value:
            birthdate_input.value = f"{date_picker.value.strftime('%d/%m/%Y')}"
        else:
            birthdate_input.value = "Ninguna"
        page.update()

    def handle_date_picker_dismiss(e):
        page.update()

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


    login_link = ft.GestureDetector(
        content=ft.Text('Iniciar Sesion', color=PRIMARY_COLOR),
        mouse_cursor=ft.MouseCursor.CLICK,
        on_tap=lambda _: print('Clickeado..'),
    )
    name_input = input_field('Nombre', value='')
    email_input = input_field('Correo Electrónico', '', input_type=ft.KeyboardType.EMAIL)
    phone_input = input_field('Teléfono', '',input_type=ft.KeyboardType.PHONE)
    country_input = input_field('País', '')
    gender_input = selection_field('Género', GENDER)
    birthdate_input = input_field('Fecha de Nacimiento','')
    birthdate_input.read_only = True 
    birthdate_input.expand = True

    open_date_picker_button = ft.IconButton(
        icon_size=20,
        bgcolor=SECONDARY_COLOR,
        icon_color=PRIMARY_COLOR,
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: page.open(date_picker), # Usa .pick_date() para mostrarlo
    )


    content = ft.Column([
        
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
    ], 
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    content = ft.Column([
        logo,
        ft.Text(
            'Kuolix | Registrarse',
            size=16,
            weight=ft.FontWeight.BOLD,
            color=PRIMARY_COLOR
        ),
        content,
        ft.TextField(
            label='Contraseña',
            password=True,
            can_reveal_password=True,
            border_radius=15,
            border_color='#D3D3D3',
            focused_border_color=PRIMARY_COLOR,
            border_width=1,
            label_style=ft.TextStyle(
                color=PRIMARY_COLOR
            )

        ),
        ft.Row([ft.Text('¿No tienes Cuenta?'),login_link], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(
            content=ft.ElevatedButton(
                text='Registrarse',
                bgcolor=PRIMARY_COLOR,
                color=PRIMARY_TEXT_COLOR,
                on_click=lambda _: page.go('/explore')
            ),
            margin=ft.margin.only(top=30),
            border_radius=15,
        ),
        
    ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )

    signup_section = ft.Container(
        content=content,
        padding=ft.padding.all(20),
        alignment=ft.alignment.center,
        border_radius=15,
        width=400,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=1,
            color=ft.Colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        margin=ft.margin.only(top=10),
    )

    sign_view = ft.View(
        controls=[signup_section],
        padding=ft.padding.all(10),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        route='/signup',
    )

    return sign_view