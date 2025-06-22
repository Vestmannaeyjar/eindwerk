import flet as ft
from datetime import datetime
from components.paginated_list import paginated_list_view
from utilities import render_row

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/tasks/"

TASK_FIELDS = [
    {"key": "deadline", "label": "Einddatum", "width": 120},
    {"key": "project", "label": "Project", "width": 100},
    {"key": "subject", "label": "Omschrijving", "width": 500},
]

FIELD_LABELS = {field["key"]: field["label"] for field in TASK_FIELDS}


def render_task_row(task, open_edit_dialog, delete_task):
    return render_row(task, TASK_FIELDS, open_edit_dialog, delete_task)


def build_task_form(current_data, on_submit, on_cancel, page):
    deadline_input = ft.TextField(label=FIELD_LABELS["deadline"])
    project_input = ft.TextField(label=FIELD_LABELS["project"])
    subject_input = ft.TextField(label=FIELD_LABELS["subject"])

    if current_data:
        try:
            dt = datetime.strptime(current_data["deadline"], "%Y-%m-%dT%H:%M:%SZ")
            deadline_input.value = dt.strftime("%d-%m-%Y %H:%M")
        except Exception:
            deadline_input.value = current_data.get("deadline", "")
        project_input.value = current_data.get("project", "")
        subject_input.value = current_data.get("subject", "")

    def handle_submit(e):
        try:
            subject = subject_input.value.strip()
            if not subject:
                raise ValueError("Omschrijving is verplicht.")

            deadline = None
            if deadline_input.value:
                dt = datetime.strptime(deadline_input.value, "%d-%m-%Y %H:%M")
                deadline = dt.isoformat()
            else:
                deadline = None

            project = project_input.value.strip()
            payload = {"deadline": deadline, "subject": subject, "project": project}
            on_submit(payload)

        except Exception as err:
            page.snack_bar.content.value = f"Error: {err}"
            page.open(page.snack_bar)
            page.update()

    return ft.Column([
        subject_input,
        deadline_input,
        ft.Row([
            ft.TextButton("Annuleer", on_click=on_cancel),
            ft.ElevatedButton("Opslaan", on_click=handle_submit)
        ], alignment=ft.MainAxisAlignment.END)
    ])


def build_task_payload():
    # This is no longer used, see inline form logic
    pass


def tasks_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Taken",
        item="taak",
        api_base_url=API_BASE_URL,
        render_item_row=render_task_row,
        build_edit_form=lambda *args: build_task_form(*args, page=page),
        build_payload=None  # Not used; logic in form
    )
