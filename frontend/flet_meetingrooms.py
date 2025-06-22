import flet as ft
from components.paginated_list import paginated_list_view
from components.dialogcontrol import dialog_controls
from utilities import render_row, render_task_header

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/meetingrooms/"

p_color = ft.Colors.PURPLE_50
ab_color = ft.Colors.PURPLE_500
but_color = ft.Colors.PURPLE_800

MEETINGROOM_FIELDS = [
    {"key": "name", "label": "Naam", "width": 400},
    {"key": "capacity", "label": "Capaciteit", "width": 100},
]

FIELD_LABELS = {field["key"]: field["label"] for field in MEETINGROOM_FIELDS}


def render_meetingroom_row(meetingroom, open_edit_dialog, delete_meetingroom, but_color):
    return render_row(meetingroom, MEETINGROOM_FIELDS, open_edit_dialog, delete_meetingroom, but_color)


def build_meetingroom_form(current_data, on_submit, on_cancel, page):
    name_input = ft.TextField(label=FIELD_LABELS["name"])
    capacity_input = ft.TextField(label=FIELD_LABELS["capacity"])

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
        dialog_controls(on_cancel, handle_submit, but_color),
    ])


def meetingrooms_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Vergaderzalen",
        item_description="vergaderzaal",
        api_base_url=API_BASE_URL,
        render_item_row=lambda meetingroom, open_edit_dialog, delete_meetingroom: render_meetingroom_row(
            meetingroom, open_edit_dialog, delete_meetingroom, but_color),
        build_edit_form=lambda *args: build_meetingroom_form(*args, page=page),
        build_payload=None,
        render_header=render_task_header(MEETINGROOM_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )
