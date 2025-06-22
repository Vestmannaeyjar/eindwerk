import flet as ft
from datetime import datetime
from components.paginated_list import paginated_list_view
from utilities import render_row

API_BASE_URL = "http://127.0.0.1:8000/api/contacts/"

CONTACT_FIELDS = [
    {"key": "firstname", "label": "First name", "width": 100},
    {"key": "lastname", "label": "Last name", "width": 100},
    {"key": "date_of_birth", "label": "Date (dd-mm-yyyy)", "width": 100},
]


def render_contact_row(contact, open_edit_dialog, delete_contact):
    return render_row(contact, CONTACT_FIELDS, open_edit_dialog, delete_contact)


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
        except Exception as err:
            page.snack_bar.content.value = f"Error: {err}"
            page.open(page.snack_bar)
            page.update()

    return ft.Column([
        *inputs.values(),
        ft.Row([
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.ElevatedButton("Save", on_click=handle_submit)
        ], alignment=ft.MainAxisAlignment.END)
    ])


def contacts_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Personen",
        item="persoon",
        api_base_url=API_BASE_URL,
        render_item_row=render_contact_row,
        build_edit_form=lambda *args: build_contact_form(*args, page=page),
        build_payload=None
    )
