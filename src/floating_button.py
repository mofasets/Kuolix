import flet as ft

PRIMARY_COLOR = ft.colors.BLUE
SECONDARY_COLOR = ft.colors.GREEN
TERTIARY_COLOR = ft.colors.ORANGE

class FloatingActionButtonsGroup(ft.Stack):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.controls = [
            self.main_fab,
            self.secondary_fab_1,
            self.secondary_fab_2,
        ]
        self.alignment = ft.alignment.bottom_right
        self.clip_behavior = ft.ClipBehavior.NONE
        self.expanded = False

    def did_mount(self):
        self.page.on(ft.PageEvent.RESIZE, self.update_position)
        self.update_position()

    def will_unmount(self):
        self.page.off(ft.PageEvent.RESIZE, self.update_position)

    def update_position(self, e=None):
        self.right = 20
        self.bottom = 20
        self.update()

    def toggle(self):
        self.expanded = not self.expanded
        self.animate_secondary_buttons()
        self.rotate_main_button()
        self.update()

    def animate_secondary_buttons(self):
        distance = 60  # Distancia entre los botones secundarios
        animation_duration = 300

        self.secondary_fab_1.animate_to(
            ft.Transform(
                translation=ft.Offset(0, -distance if self.expanded else 0),
                origin=ft.Offset(0.5, 0.5),
            ),
            duration=animation_duration,
            curve=ft.AnimationCurve.EASE_OUT,
        )
        self.secondary_fab_2.animate_to(
            ft.Transform(
                translation=ft.Offset(0, -2 * distance if self.expanded else 0),
                origin=ft.Offset(0.5, 0.5),
            ),
            duration=animation_duration,
            curve=ft.AnimationCurve.EASE_OUT,
        )

    def rotate_main_button(self):
        animation_duration = 200
        self.main_fab.rotate = ft.transform.Rotate(
            angle=0.25 if self.expanded else 0,  # Rotar 90 grados al expandir
            origin=ft.Offset(0.5, 0.5),
        )
        self.main_fab.update()

    @property
    def main_fab(self):
        return ft.FloatingActionButton(
            icon=ft.icons.ADD,
            bgcolor=PRIMARY_COLOR,
            foreground_color=ft.colors.WHITE,
            on_click=self.toggle,
        )

    @property
    def secondary_fab_1(self):
        return ft.AnimatedContainer(
            content=ft.FloatingActionButton(
                icon=ft.icons.IMAGE,
                bgcolor=SECONDARY_COLOR,
                foreground_color=ft.colors.WHITE,
                mini=True,
                on_click=lambda _: print("¡Botón secundario 1 clickeado!"),
            ),
            duration=300,
            transform=ft.Transform(translation=ft.Offset(0, 0)),
            transform_origin=ft.Offset(0.5, 0.5),
        )

    @property
    def secondary_fab_2(self):
        return ft.AnimatedContainer(
            content=ft.FloatingActionButton(
                icon=ft.icons.CAMERA_ALT,
                bgcolor=TERTIARY_COLOR,
                foreground_color=ft.colors.WHITE,
                mini=True,
                on_click=lambda _: print("¡Botón secundario 2 clickeado!"),
            ),
            duration=300,
            transform=ft.Transform(translation=ft.Offset(0, 0)),
            transform_origin=ft.Offset(0.5, 0.5),
        )

def main(page: ft.Page):
    page.title = "Menú FAB Desplegable"
    page.add(FloatingActionButtonsGroup(page))

if __name__ == "__main__":
    ft.app(target=main)