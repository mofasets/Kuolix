import flet as ft
from components.logo import logo
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR,BACKGROUND_COLOR, PRIMARY_TEXT_COLOR

def get_login_view(page: ft.Page) -> ft.View:
    signup_link = ft.GestureDetector(
        content=ft.Text('Registrate', color=PRIMARY_COLOR),
        mouse_cursor=ft.MouseCursor.CLICK,
        on_tap=lambda _: page.go('/signup'),
    )

    content = ft.Column([
        logo,
        ft.Text(
            'Kuolix | Inicio de Sesión',
            size=16,
            weight=ft.FontWeight.BOLD,
            color=PRIMARY_COLOR
        ),
        ft.TextField(
            label='Correo',
            keyboard_type=ft.KeyboardType.EMAIL,
            border_radius=15,
            border_color='#D3D3D3',
            focused_border_color=PRIMARY_COLOR,
            border_width=1,
            label_style=ft.TextStyle(
                color=PRIMARY_COLOR
            )
        ),
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
        ft.Row([ft.Text('¿No tienes Cuenta?'),signup_link], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(
            content=ft.ElevatedButton(
                text='Iniciar Sesión',
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

    login_section = ft.Container(
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
        margin=ft.margin.only(top=100),
    )


    login_view = ft.View(
        controls=[login_section],
        padding=ft.padding.all(10),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        route='/login',
    )

    return login_view
