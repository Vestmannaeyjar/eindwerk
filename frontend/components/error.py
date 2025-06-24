import flet as ft

error_container = ft.Container(visible=False)


def show_error(message, container, page):
    """Show error message in the form using in-dialog container."""
    container.content = ft.Row([
        ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=20),
        ft.Text(message, color=ft.Colors.RED, expand=True, size=14)
    ])
    container.bgcolor = ft.Colors.RED_50
    container.border = ft.border.all(1, ft.Colors.RED_200)
    container.border_radius = 5
    container.padding = 10
    container.visible = True
    page.update()
