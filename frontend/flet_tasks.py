import flet as ft
from datetime import datetime
from components.paginated_list import paginated_list_view

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/tasks/"


def render_task_row(task, open_edit_dialog, delete_task):
    return ft.Row([
        ft.Text(f"{task['subject']} (Deadline: {task.get('deadline', 'N/A')})", expand=True),
        ft.IconButton(icon="edit", tooltip="Edit", on_click=lambda e: open_edit_dialog(task)),
        ft.IconButton(icon="delete", tooltip="Delete", on_click=lambda e: delete_task(task["id"])),
    ])


def build_task_form(current_data, on_submit, on_cancel, page):
    subject_input = ft.TextField(label="Subject")
    deadline_input = ft.TextField(label="Deadline (dd-mm-yyyy HH:MM)")

    if current_data:
        subject_input.value = current_data.get("subject", "")
        try:
            dt = datetime.strptime(current_data["deadline"], "%Y-%m-%dT%H:%M:%SZ")
            deadline_input.value = dt.strftime("%d-%m-%Y %H:%M")
        except Exception:
            deadline_input.value = current_data.get("deadline", "")

    def handle_submit(e):
        try:
            subject = subject_input.value.strip()
            if not subject:
                raise ValueError("Subject is required.")

            deadline = None
            if deadline_input.value:
                dt = datetime.strptime(deadline_input.value, "%d-%m-%Y %H:%M")
                deadline = dt.isoformat()
            else:
                deadline = None

            payload = {"subject": subject, "deadline": deadline}
            on_submit(payload)

        except Exception as err:
            page.snack_bar.content.value = f"Error: {err}"
            page.open(page.snack_bar)
            page.update()

    return ft.Column([
        subject_input,
        deadline_input,
        ft.Row([
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.ElevatedButton("Save", on_click=handle_submit)
        ], alignment=ft.MainAxisAlignment.END)
    ])


def build_task_payload():
    # This is no longer used, see inline form logic
    pass


def tasks_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Tasks",
        api_base_url=API_BASE_URL,
        render_item_row=render_task_row,
        build_edit_form=lambda *args: build_task_form(*args, page=page),
        build_payload=None  # Not used; logic in form
    )
