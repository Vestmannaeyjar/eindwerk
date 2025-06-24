import flet as ft


def dialog_controls(on_cancel, handle_submit):
    return ft.Row([
        ft.ElevatedButton("Annuleer", on_click=on_cancel, color=ft.Colors.RED_500, icon=ft.Icons.CANCEL),
        ft.ElevatedButton("Opslaan", on_click=handle_submit, color=ft.Colors.GREEN_500, icon=ft.Icons.CHECK)
        ], alignment=ft.MainAxisAlignment.END)
