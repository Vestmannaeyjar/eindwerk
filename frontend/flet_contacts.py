import flet as ft
from datetime import datetime
from components.paginated_list import paginated_list_view
from components.dialogcontrol import dialog_controls
from components.error import error_container, show_error
from utilities import render_row, render_task_header

API_BASE_URL = "http://127.0.0.1:8000/api/contacts/"

p_color = ft.Colors.RED_50
ab_color = ft.Colors.RED_500
but_color = ft.Colors.RED_800

CONTACT_FIELDS = [
    {"key": "firstname", "label": "Voornaam", "width": 200},
    {"key": "lastname", "label": "Familienaam", "width": 200},
    {"key": "date_of_birth", "label": "Geboortedatum", "width": 200, "type": "date"},
]

FIELD_LABELS = {field["key"]: field["label"] for field in CONTACT_FIELDS}


def render_contact_row(contact, open_edit_dialog, delete_contact, but_color):
    return render_row(contact, CONTACT_FIELDS, open_edit_dialog, delete_contact, but_color)


def build_contact_form(current_data, on_submit, on_cancel, page):
    inputs = {}
    for field in CONTACT_FIELDS:
        key = field["key"]
        inputs[key] = ft.TextField(label=field["label"])
        if current_data and key in current_data:
            value = current_data[key]
            if key == "date_of_birth":
                try:
                    value = datetime.strptime(value, "%Y-%m-%d").strftime("%d-%m-%Y")
                except:
                    pass
            inputs[key].value = value

    def handle_submit(e):
        try:
            dob = datetime.strptime(inputs["date_of_birth"].value.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
            payload = {
                "firstname": inputs["firstname"].value.strip(),
                "lastname": inputs["lastname"].value.strip(),
                "date_of_birth": dob,
            }
            on_submit(payload)
        except Exception as e:
            show_error(f"Error: {e}", error_container, page)

    return ft.Column([
        *inputs.values(),
        error_container,
        dialog_controls(on_cancel, handle_submit, but_color),
    ])


def contacts_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Personen",
        item_description="persoon",
        api_base_url=API_BASE_URL,
        render_item_row=lambda contact, open_edit_dialog, delete_contact: render_contact_row(
            contact, open_edit_dialog, delete_contact, but_color),
        build_edit_form=lambda *args: build_contact_form(*args, page=page),
        build_payload=None,
        render_header=render_task_header(CONTACT_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )
