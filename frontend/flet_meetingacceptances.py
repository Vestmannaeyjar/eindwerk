import flet as ft
from datetime import datetime
import requests
from components.paginated_list import paginated_list_view

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/meetingacceptances/"

def render_meetingacceptance_row(meetingacceptance, open_edit_dialog, delete_meetingacceptance):
    return ft.Row([
        ft.Text(f"{meetingacceptance['name']}", expand=True),
        ft.IconButton(icon="edit", tooltip="Edit", on_click=lambda e: open_edit_dialog(meetingacceptance)),
        ft.IconButton(icon="delete", tooltip="Delete", on_click=lambda e: delete_meetingacceptance(meetingacceptance["id"])),
    ])


def build_meetingacceptance_form(current_data, on_submit, on_cancel, page):
    name_input = ft.TextField(label="Name")

    if current_data:
        name_input.value = current_data.get("name", "")

    def handle_submit(e):
        try:
            payload = {
                "name": name_input.value.strip(),
            }
            on_submit(payload)
        except Exception as err:
            page.snack_bar.content.value = f"Error: {err}"
            page.open(page.snack_bar)
            page.update()

    return ft.Column([
        name_input,
        ft.Row([
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.ElevatedButton("Save", on_click=handle_submit)
        ], alignment=ft.MainAxisAlignment.END)
    ])


def meetingacceptances_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Meetingacceptances",
        api_base_url=API_BASE_URL,
        render_item_row=render_meetingacceptance_row,
        build_edit_form=lambda *args: build_meetingacceptance_form(*args, page=page),
        build_payload=None
    )
