import flet as ft
import base64
from components.loading import get_loading_control
from sources.colors_pallete import PRIMARY_COLOR, SECONDARY_COLOR
from components.input_field import input_field
from components.selection_field import selection_field
import httpx
from state import AppState
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_BASE_URL")
IMG_URL = f"{API_URL}/static/images/plants/no-image.jpg"

class EditView(ft.View):

    def __init__(self, page: ft.Page, item_id: str, app_state: AppState,):
        super().__init__()
        self.page = page
        self.item_id = item_id
        self.app_state = app_state
        self.route = f"/edit/{self.item_id}"
        self.scroll = ft.ScrollMode.AUTO
        self.padding = ft.padding.all(0)
        self.loading_control = get_loading_control(self.page, "Cargando detalles...")
        self.controls = [self.loading_control]

        self.info_text = ft.Text(value="", visible=False)

        self.upload_img_button = ft.IconButton(
            icon=ft.Icons.UPLOAD_FILE, 
            bgcolor=SECONDARY_COLOR,
            icon_color=PRIMARY_COLOR,
            on_click=self.load_image_click
        )

        self.remove_img_button = ft.IconButton(
            icon=ft.Icons.DELETE, 
            bgcolor=SECONDARY_COLOR,
            icon_color=PRIMARY_COLOR,
            on_click=self.delete_image_click
        )

        self.edit_item_button = ft.ElevatedButton(
            'Editar Planta',
            color=SECONDARY_COLOR,
            bgcolor=PRIMARY_COLOR,
            on_click=self.edit_item
        )

        self.discard_item_button = ft.ElevatedButton(
            'Cancelar',
            color=PRIMARY_COLOR,
            bgcolor=SECONDARY_COLOR,
            on_click=self.go_back
        )
        self.scientific_name_input = input_field('Nombre Científico', '')
        self.common_names_input = input_field('Nombres Comunes', '', placeholder='Separe los nombres por comas (,)', multiline=True)
        self.habitat_description_input = input_field('Descripción del Habitat', '',multiline=True)
        self.general_ailments_input = input_field('Malestares Generales','',multiline=True)
        self.specific_diseases_input =  input_field('Malestares Específicos','',placeholder='Separe los nombres por comas (,)',multiline=True)
        self.usage_instructions_input = input_field('Instrucciones de Uso', '',multiline=True)
        self.taxonomy_input = input_field('Taxonomía', '',multiline=True)
        self.active_ingredient_input = input_field('Ingrediente Activo', '',multiline=True)
        self.references_input = input_field('Referencias', '', placeholder="Separe por punto y coma (;)" , multiline=True)
        self.safety_level_input = selection_field('Tipo Planta',['Medicinal', 'Neutral', 'Toxic'])
        self.is_verified_switch = ft.Switch(
            'Verificado', 
            active_color=SECONDARY_COLOR,
            active_track_color=PRIMARY_COLOR, 
            inactive_thumb_color=ft.Colors.GREY_400,
            inactive_track_color=ft.Colors.GREY_300,
            value=False
        )

        #Image Fields.
        self.image_bytes = None

        self.item_image = ft.Container(
            content=ft.Image(
                src=IMG_URL, 
                fit=ft.ImageFit.COVER,
                width=250,
                height=250,
                border_radius=60,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
        )

        self.file_picker = ft.FilePicker(on_result=self.on_file_picker_result)
        if self.file_picker not in self.page.overlay:
            self.page.overlay.append(self.file_picker)
        
        self.page.run_task(self.fetch_and_display_data)

    async def fetch_details_from_api_async(self, item_id: str) -> dict:
        """
        Realiza una llamada a la API para obtener los detalles de una planta por su ID.
        """
        
        token = self.app_state.token
        if not token:
            self.page.go("/login")
            return {}

        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = await self.app_state.api_client.get(
                f"/show/{item_id}", 
                headers=headers
            )
            response.raise_for_status()
            
            print("Detalles recibidos con éxito.")
            return response.json()

        except httpx.HTTPStatusError as exc:
            print(f"Error de API: {exc.response.status_code} - {exc.response.text}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
        
        # En caso de error, devuelve un objeto por defecto para no romper la UI.
        return {
            "scientific_name": response.get('scientific_name', 'Sin Información'),
            "common_names": response.get('common_names',[]),
            "habitat_description": response.get('habitat_description','Sin Información'),
            "specific_deseases": response.get('specific_deseases',[]),
            "usage_instructions": response.get('usage_instructions','Sin Información'),
            "image": f"{API_URL}/static/images/plants/{response.get('image_filename','no-image.jpg')}",
        }

    async def fetch_and_display_data(self) -> dict:
        """
        Busca los datos del elemento y construye la UI final.
        """
        data = await self.fetch_details_from_api_async(self.item_id)

        self.build_ui(data)
        self.page.update()

    def build_ui(self, data: dict):
        """
        Construye la interfaz de usuario con los datos proporcionados.
        """

        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK, 
            on_click=self.go_back, 
            icon_color=PRIMARY_COLOR, 
            icon_size=30
        )

        img_buttons = ft.Row(
            [self.upload_img_button, self.remove_img_button], 
            alignment=ft.MainAxisAlignment.CENTER, 
            spacing=30,
        )

        self.scientific_name_input.value = data.get('scientific_name','')
        self.common_names_input.value = ','.join(data.get('common_names',[]))
        self.habitat_description_input.value = data.get('habitat_description','')
        self.general_ailments_input.value = data.get('general_ailments','')
        self.specific_diseases_input.value = ','.join(data.get('specific_diseases',[]))
        self.usage_instructions_input.value = data.get('usage_instructions','')
        self.taxonomy_input.value = data.get('taxonomy','')
        self.active_ingredient_input.value = data.get('active_ingredient','')
        self.references_input.value = ';'.join(data.get('references',[]))
        self.safety_level_input.value = data.get('safety_level','')
        self.is_verified_switch.value = data.get('is_verified',False)

        #Get Filename
        self.item_image.content.src = f"{API_URL}/static/images/plants/{data.get('image_filename','no-image.jpg')}"


        form_content = ft.Column([
            self.scientific_name_input,
            self.common_names_input,
            self.habitat_description_input,
            self.general_ailments_input,
            self.specific_diseases_input,
            self.usage_instructions_input,
            self.taxonomy_input,
            self.active_ingredient_input,
            self.references_input,
            self.safety_level_input,
            self.is_verified_switch
        ])

        item_buttons = ft.Row([
            self.edit_item_button,
            self.discard_item_button
        ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER
        )

        content_column = ft.Column([
            back_button,
            self.item_image,
            img_buttons,
            form_content,
            self.info_text,
            item_buttons
        ])

        self.controls.clear()
        self.controls.append(ft.Container(content=content_column, padding=ft.padding.only(top=20, left=10, right=10, bottom=20)))

    async def go_back(self, e):
        """
        Navega a la vista anterior en la pila de vistas.
        """
        if len(self.page.views) > 1:
            previous_view_route = self.page.views[-2].route
            self.page.go(previous_view_route)
        else:
            self.page.go("/search")

    def load_image_click(self, e: ft.ControlEvent):

        # Open File Picker
        self.file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    def delete_image_click(self, e: ft.ControlEvent):

        self.image_bytes = None
        
        # Restablece la imagen al placeholder
        self.item_image.content.src = IMG_URL
        self.item_image.content.src_base64 = None
        
        # Deshabilita el botón de borrar
        self.remove_img_button.disabled = True
        
        self.page.update()

    async def on_file_picker_result(self, e: ft.FilePickerResultEvent):

        if not e.files:
            print("El usuario canceló la selección.")
            return

        # Obtener el archivo seleccionado
        selected_file = e.files[0]
        print(f"Archivo seleccionado: {selected_file.name}")

        try:
            with open(selected_file.path, "rb") as f:
                if f is not None:
                    self.image_bytes = f.read()
            
            self.item_image.content.src = ''
            self.item_image.content.src_base64 = base64.b64encode(self.image_bytes).decode('utf-8') 
            
            self.remove_img_button.disabled = False
            
            self.page.update()

        except Exception as ex:
            print(f"Error al leer el archivo: {ex}")

    async def edit_item(self, e: ft.ControlEvent):
        self.edit_item_button.disabled = True
        self.page.update()

        data = {
            "scientific_name": self.scientific_name_input.value,
            "common_names": self.common_names_input.value,
            "habitat_description": self.habitat_description_input.value,
            "general_ailments": self.general_ailments_input.value,
            "specific_diseases": self.specific_diseases_input.value,
            "usage_instructions":self.usage_instructions_input.value,
            "taxonomy":self.taxonomy_input.value,
            "active_ingredient":self.active_ingredient_input.value,
            "references":self.references_input.value,
            "safety_level":self.safety_level_input.value,
            "is_verified":self.is_verified_switch.value,
        }

        try:

            campos_texto_obligatorios = [
                data["scientific_name"],
                data["common_names"],
                data["habitat_description"],
                data["general_ailments"],
                data["specific_diseases"],
                data["usage_instructions"],
                data["taxonomy"],
                data["active_ingredient"],
                data["references"],
                data["safety_level"]
            ]

            if any(not value for value in campos_texto_obligatorios):
                raise ValueError('Error: Debe llenar todos los campos del formulario.')

        except ValueError as e: #
            self.info_text.value = str(e) 
            self.info_text.color = ft.Colors.RED_500
            self.info_text.visible = True
            
            self.edit_item_button.disabled = False
            self.page.update()
            
            return
        
        try:
            if any(value in ['', False] for value in data.values()):
                raise ValueError('Debes llenar todos los campos')
        except:
            error_message = 'Debes llenar todos los campos'
            self.info_text.value = error_message
            self.info_text.color = ft.Colors.RED
            self.info_text.visible = True

        str_data = {
            "data": json.dumps(data)
        }

        files_data = None

        if self.image_bytes:
            files_data = {
                "img": (
                    f"{self.scientific_name_input.value.lower().replace(' ', '_')}.jpg", 
                    self.image_bytes, 
                    "image/jpeg"
                )
            }

        token = self.app_state.token
        if not token:
            self.page.go("/login")
            return

        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = await self.app_state.api_client.put(
                f"/plant/edit",
                headers=headers,
                data=str_data,
                files=files_data
            )
            response.raise_for_status()
            self.page.open(ft.SnackBar(content=ft.Text('Planta actualizado con éxito.', color="white"), bgcolor=ft.Colors.GREEN_400, duration=1000))
            self.edit_item_button.disabled = False
            self.page.update()
            
            return response.json()
            
        except Exception as ex:
            print(ex)
            self.page.open(ft.SnackBar(content=ft.Text('Error al Actualizar Datos', color="white"), bgcolor=ft.Colors.RED_400, duration=1000))    

