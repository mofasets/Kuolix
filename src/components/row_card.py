import flet as ft
from sources.colors_pallete import BACKGROUND_COLOR, PRIMARY_COLOR, DANGER_TITLE_COLOR, DARGER_BG_COLOR
from components.badge import badge
import os
from dotenv import load_dotenv
from state import app_state
import httpx
from typing import Callable, Optional

load_dotenv()
API_URL = os.getenv("API_BASE_URL")


def row_card(page: ft.Page, content: dict[str, str], back_route: str, on_delete_callback: Optional[Callable] = None) -> ft.Container:
    confirm_dialog = ft.AlertDialog()
    
    def close_dialog_sync(e: ft.ControlEvent = None):
        """Cierra el modal (versión síncrona)."""
        if confirm_dialog:
            confirm_dialog.open = False
            page.update()

    async def delete_record_confirmed(itemid: str):
        """Llama a la API para borrar y luego llama al callback."""
        
        token = app_state.token
        if not token:
            page.go("/login")
            close_dialog_sync()
            return

        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = await app_state.api_client.delete(
                f"/plant/delete/{itemid}", 
                headers=headers
            )
            response.raise_for_status() 

            page.open(
                ft.SnackBar(
                    ft.Text("Registro eliminado con éxito"), 
                    bgcolor=ft.Colors.GREEN_400,
                    duration=2000
                )
            )
            if on_delete_callback:
                await on_delete_callback() 

        except httpx.HTTPStatusError as exc:
            error_detail = exc.response.json().get("detail", "Error")
            page.open(ft.SnackBar(ft.Text(f"Error de API: {error_detail}"), bgcolor=ft.Colors.RED_400))
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Error de conexión: {ex}"), bgcolor=ft.Colors.RED_400))
        
        close_dialog_sync()
        page.update()

    def open_delete_dialog(itemid: str, item_name: str):
        """Construye y muestra el modal de confirmación."""
        nonlocal confirm_dialog
        
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Está seguro de que desea eliminar '{item_name}'?\n\nEsta acción no se puede deshacer."),
            actions=[
                ft.TextButton(
                    "No, Cancelar",
                    on_click=close_dialog_sync
                ),
                ft.TextButton(
                    "Sí, Eliminar",
                    style=ft.ButtonStyle(color=ft.Colors.RED_500),
                    on_click=lambda e: page.run_task(
                        delete_record_confirmed, 
                        itemid
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(confirm_dialog)
        confirm_dialog.open = True
        page.update()

    def on_click(e):
        page.session.set("id", content.get("id"))
        page.session.set("scientific_name", content.get("scientific_name"))
        page.session.set("common_names", content.get("common_names"))
        page.session.set("habitat_description", content.get("habitat_description"))
        page.session.set("specific_diseases", content.get("specific_diseases"))
        page.session.set("back_route", back_route)
        page.go(f'/show/{content.get("id")}')

    image_url = f"{API_URL}/static/images/plants/{content.get('image_filename','no-image.jpg')}"

    plant_image = ft.Image(
        src=image_url,
        fit=ft.ImageFit.COVER, 
        border_radius=ft.border_radius.all(15),
        error_content=ft.Image(
            src='img/logo.png',
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(15),
        )
    )
    #Role.
    user_role = "aficionado"
    if app_state.current_user:
        user_role = app_state.current_user.get("role", "aficionado")

    # Buttons
    edit_plant_button = ft.IconButton(
        icon=ft.Icons.EDIT_NOTE, 
        icon_color=PRIMARY_COLOR, 
        bgcolor=BACKGROUND_COLOR,
        on_click=lambda _:page.go(f'/edit/{content.get("id")}')
    )

    delete_plant_button = ft.IconButton(
        icon=ft.Icons.DELETE, 
        icon_color=DANGER_TITLE_COLOR, 
        bgcolor=DARGER_BG_COLOR,
        on_click=lambda e, itemid=content.get('id'), item_name=content.get('scientific_name'): open_delete_dialog(itemid, item_name)
    )

    admin_buttons_row = ft.Row(
        [edit_plant_button, delete_plant_button],
        alignment=ft.MainAxisAlignment.END,
        visible=(user_role == "admin")
    )

    #Badges with the specific deseases.
    specific_deseases_badges = ft.Container()
    if content.get('specific_diseases'):
        specific_deseases_badges.content = ft.Row([badge(desease) for desease in content.get('specific_diseases')], wrap=True)

    control_content = ft.Row([
        ft.Column([
            admin_buttons_row,
            ft.Container(content=plant_image, alignment=ft.alignment.center),
            ft.Text(content.get('scientific_name'), color=PRIMARY_COLOR, size=24, weight=ft.FontWeight.BOLD),
            specific_deseases_badges,
            ft.Text(f'{content.get("habitat_description", "")[:100]}...', size=16)
        ], 
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )],
        spacing=20,
    )

    row_card = ft.Container(
        content=control_content,
        padding=ft.padding.only(left=10, right=10, top=10, bottom=30),
        border_radius=15,
        margin=ft.margin.only(bottom=10),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=3,
            color="#CCCCCC",
            offset=ft.Offset(0, 1),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        on_click=on_click,
    )

    return row_card