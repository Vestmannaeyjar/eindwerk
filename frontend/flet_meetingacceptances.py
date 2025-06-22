import flet as ft
from components.paginated_list import paginated_list_view
from components.dialogcontrol import dialog_controls
from utilities import render_row, render_task_header

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/meetingacceptances/"

p_color = ft.Colors.ORANGE_50
ab_color = ft.Colors.ORANGE_500
but_color = ft.Colors.ORANGE_800

MEETINGACCEPTANCE_FIELDS = [
    {"key": "name", "label": "Naam", "width": 300},
]

FIELD_LABELS = {field["key"]: field["label"] for field in MEETINGACCEPTANCE_FIELDS}


def render_meetingacceptance_row(meetingacceptance, open_edit_dialog, delete_meetingacceptance, but_color):
    return render_row(meetingacceptance, MEETINGACCEPTANCE_FIELDS, open_edit_dialog, delete_meetingacceptance, but_color)


def build_meetingacceptance_form(current_data, on_submit, on_cancel, page):
    name_input = ft.TextField(label=FIELD_LABELS["name"])

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
        dialog_controls(on_cancel, handle_submit, but_color),
    ])


def meetingacceptances_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Status deelnemers",
        item_description="deelnemerstatus",
        api_base_url=API_BASE_URL,
        render_item_row=lambda meetingacceptance, open_edit_dialog, delete_meetingacceptance: render_meetingacceptance_row(
            meetingacceptance, open_edit_dialog, delete_meetingacceptance, but_color),
        build_edit_form=lambda *args: build_meetingacceptance_form(*args, page=page),
        build_payload=None,
        render_header=render_task_header(MEETINGACCEPTANCE_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )
