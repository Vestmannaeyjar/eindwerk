import flet as ft
import requests
from datetime import datetime
from components.datetime_functions import parse_iso_datetime
from components.paginated_list import paginated_list_view
from components.dialogcontrol import dialog_controls
from components.error import error_container, show_error
from utilities import render_row, render_task_header

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/tasks/"
PROJECTS_URL = "http://127.0.0.1:8000/api/tasks/projects/"
CONTEXTCONTACTS_URL = "http://127.0.0.1:8000/api/contextcontacts/"

p_color = ft.Colors.BLUE_50
ab_color = ft.Colors.BLUE_500
but_color = ft.Colors.BLUE_900

TASK_FIELDS = [
    {"key": "deadline", "label": "Einddatum", "width": 200, "type": "datetime"},
    {"key": "project", "label": "Project", "width": 150, "display_key": "project_name"},
    {"key": "subject", "label": "Omschrijving", "width": 300},
    {"key": "assignment", "label": "Verantwoordelijke", "width": 200, "display_key": "contextcontact_name"},
]

FIELD_LABELS = {field["key"]: field["label"] for field in TASK_FIELDS}


def render_task_row(task, open_edit_dialog, delete_task, but_color):
    return render_row(task, TASK_FIELDS, open_edit_dialog, delete_task, but_color)


def build_task_form(current_data, on_submit, on_cancel, page):
    deadline_input = ft.TextField(label=FIELD_LABELS["deadline"])
    project_input = ft.Dropdown(
        label=FIELD_LABELS["project"],
        hint_text="Selecteer een project...",
        options=[],
    )
    subject_input = ft.TextField(label=FIELD_LABELS["subject"])
    assignment_input = ft.Dropdown(
        label=FIELD_LABELS["assignment"],
        hint_text="Selecteer een verantwoordelijke...",
        options=[],
    )

    async def load_projects():

        project_input.disabled = True
        project_input.hint_text = "Projecten laden..."
        page.update()

        try:
            res = requests.get(PROJECTS_URL, timeout=5)
            res.raise_for_status()
            data = res.json()
            projects = data.get("results", data)
            project_input.options = [
                ft.dropdown.Option(key=str(project["id"]), text=project["name"])
                for project in projects
            ]
            project_input.hint_text = "Selecteer een project..."
        except requests.RequestException as e:
            show_error(f"Kon projecten niet laden: {e}", error_container, page)
        except Exception as e:
            show_error(f"Onverwachte fout: {e}", error_container, page)
        finally:
            project_input.disabled = False
            page.update()

    async def load_contextcontacts():
        assignment_input.disabled = True
        assignment_input.hint_text = "Personen laden..."
        page.update()

        try:
            res = requests.get(CONTEXTCONTACTS_URL, timeout=5)
            res.raise_for_status()
            data = res.json()
            contextcontacts = data.get("results", data)
            assignment_input.options = [
                ft.dropdown.Option(key=str(contextcontact["id"]), text=contextcontact["contextcontact_name"])
                for contextcontact in contextcontacts
            ]
            assignment_input.hint_text = "Selecteer een verantwoordelijke..."
        except requests.RequestException as e:
            show_error(f"Kon personen in context niet laden: {e}", error_container, page)
        except Exception as e:
            show_error(f"Onverwachte fout: {e}", error_container, page)
        finally:
            assignment_input.disabled = False
            page.update()

    page.run_task(load_projects)
    page.run_task(load_contextcontacts)

    if current_data:
        deadline_input.value = parse_iso_datetime(current_data.get("deadline", ""))
        if current_data.get("project"):
            project_input.value = str(current_data.get("project"))
        subject_input.value = current_data.get("subject", "")
        if current_data.get("assignment"):
            assignment_input.value = str(current_data.get("assignment"))

    def parse_deadline(deadline_str):
        """Parse deadline string to ISO format."""
        if not deadline_str or not deadline_str.strip():
            return None

        try:
            dt = datetime.strptime(deadline_str.strip(), "%d-%m-%Y %H:%M")
            return dt.isoformat()
        except ValueError:
            raise ValueError("Ongeldige datum/tijd format. Gebruik dd-mm-jjjj hh:mm")

    def validate_form_data():
        """Validate form inputs and return cleaned data."""
        # Validate subject
        subject = subject_input.value.strip() if subject_input.value else ""
        if not subject:
            raise ValueError("Omschrijving is verplicht.")

        # Parse deadline
        deadline = parse_deadline(deadline_input.value)

        # Clean project
        project_id = None
        if project_input.value:
            try:
                project_id = int(project_input.value)
            except ValueError:
                project_id = project_input.value

        contact_id = None
        if assignment_input.value:
            try:
                contact_id = int(assignment_input.value)
            except ValueError:
                contact_id = assignment_input.value

        return {
            "deadline": deadline,
            "subject": subject,
            "project": project_id,
            "assignment": contact_id,
        }

    def handle_submit():
        try:
            payload = validate_form_data()
            on_submit(payload)
        except ValueError as validation_err:
            show_error(str(validation_err), error_container, page)
        except Exception as e:
            show_error(f"Fout bij opslaan: {e}", error_container, page)

    return ft.Column([
        subject_input,
        deadline_input,
        project_input,
        assignment_input,
        error_container,
        dialog_controls(on_cancel, handle_submit, but_color),
    ], width=400, spacing=10)


def build_task_payload():
    # This is no longer used, see inline form logic
    pass


def tasks_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Taken",
        item_description="taak",
        api_base_url=API_BASE_URL,
        render_item_row=lambda task, open_edit_dialog, delete_task: render_task_row(
            task, open_edit_dialog, delete_task, but_color),
        build_edit_form=lambda *args: build_task_form(*args, page=page),
        build_payload=None,  # Not used; logic in form
        render_header=render_task_header(TASK_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )
