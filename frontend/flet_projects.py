import flet as ft
from components.paginated_list import paginated_list_view
from components.dialogcontrol import dialog_controls
from components.error import error_container, show_error
from utilities import render_row, render_task_header

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/projects/"

p_color = ft.Colors.PINK_50
ab_color = ft.Colors.PINK_500
but_color = ft.Colors.PINK_800

PROJECT_FIELDS = [
    {"key": "name", "label": "Naam", "width": 400},
    {"key": "startdate", "label": "Start", "width": 400},
    {"key": "enddate", "label": "Einde", "width": 400},
]

FIELD_LABELS = {field["key"]: field["label"] for field in PROJECT_FIELDS}


def render_project_row(project, open_edit_dialog, delete_project, button_color):
    return render_row(project, PROJECT_FIELDS, open_edit_dialog, delete_project, button_color)


def build_project_form(current_data, on_submit, on_cancel, page):
    name_input = ft.TextField(label=FIELD_LABELS["name"])
    startdate_input = ft.TextField(label=FIELD_LABELS["startdate"])
    enddate_input = ft.TextField(label=FIELD_LABELS["enddate"])

    if current_data:
        name_input.value = current_data.get("name", "")
        startdate_input.value = current_data.get("name", "")
        enddate_input.value = current_data.get("name", "")

    def handle_submit(_):
        try:
            payload = {
                "name": name_input.value.strip(),
            }
            on_submit(payload)
        except Exception as e:
            show_error(f"Error: {e}", error_container, page)

    return ft.Column([
        name_input,
        error_container,
        dialog_controls(on_cancel, handle_submit),
    ])


def projects_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Projecten",
        item_description="project",
        api_base_url=API_BASE_URL,
        render_item_row=lambda project, open_edit_dialog, delete_project: render_project_row(
            project, open_edit_dialog, delete_project, but_color),
        build_edit_form=lambda *args: build_project_form(*args, page=page),
        render_header=render_task_header(PROJECT_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )
