import flet as ft
from components.paginated_list import paginated_list_view
from utilities import render_row

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/meetingrooms/"

MEETINGROOM_FIELDS = [
    {"key": "name", "label": "Name", "width": 100},
    {"key": "capacity", "label": "Capacity", "width": 50},
]


def render_meetingroom_row(meetingroom, open_edit_dialog, delete_meetingroom):
    return render_row(meetingroom, MEETINGROOM_FIELDS, open_edit_dialog, delete_meetingroom)


def build_meetingroom_form(current_data, on_submit, on_cancel, page):
    name_input = ft.TextField(label="Name")
    capacity_input = ft.TextField(label="Capacity")

    if current_data:
        name_input.value = current_data.get("name", "")
        capacity_input.value = current_data.get("capacity", "")

    def handle_submit(e):
        try:
            payload = {
                "name": name_input.value.strip(),
                "capacity": capacity_input.value,
            }
            on_submit(payload)
        except Exception as err:
            page.snack_bar.content.value = f"Error: {err}"
            page.open(page.snack_bar)
            page.update()

    return ft.Column([
        name_input,
        capacity_input,
        ft.Row([
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.ElevatedButton("Save", on_click=handle_submit)
        ], alignment=ft.MainAxisAlignment.END)
    ])


def meetingrooms_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Vergaderzalen",
        item_description="vergaderzaal",
        api_base_url=API_BASE_URL,
        render_item_row=render_meetingroom_row,
        build_edit_form=lambda *args: build_meetingroom_form(*args, page=page),
        build_payload=None
    )
