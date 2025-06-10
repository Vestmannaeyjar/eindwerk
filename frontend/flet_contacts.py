import flet as ft
from datetime import datetime
import requests
from components.paginated_list import paginated_list_view

API_BASE_URL = "http://127.0.0.1:8000/api/contacts/"


def render_contact_row(contact, open_edit_dialog, delete_contact):
    return ft.Row([
        ft.IconButton(icon="edit", tooltip="Edit", on_click=lambda e: open_edit_dialog(contact)),
        ft.IconButton(icon="delete", tooltip="Delete", on_click=lambda e: delete_contact(contact["id"])),
        ft.Text(f"{contact['firstname']}"),
        ft.Text(f"{contact['lastname']}"),
        ft.Text(f"{contact['date_of_birth']}"),
    ])


def build_contact_form(current_data, on_submit, on_cancel, page):
    firstname_input = ft.TextField(label="First name")
    lastname_input = ft.TextField(label="Last name")
    date_input = ft.TextField(label="Date (dd-mm-yyyy)")

    if current_data:
        firstname_input.value = current_data.get("firstname", "")
        lastname_input.value = current_data.get("lastname", "")
        date_str = current_data.get("date_of_birth", "")
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            date_input.value = dt.strftime("%d-%m-%Y")
        except:
            date_input.value = date_str

    def handle_submit(e):
        try:
            dob_raw = date_input.value.strip()
            # Convert from dd-mm-yyyy to yyyy-mm-dd
            dob = datetime.strptime(dob_raw, "%d-%m-%Y").strftime("%Y-%m-%d")

            payload = {
                "firstname": firstname_input.value.strip(),
                "lastname": lastname_input.value.strip(),
                "date_of_birth": dob,
            }
            on_submit(payload)
        except Exception as err:
            page.snack_bar.content.value = f"Error: {err}"
            page.open(page.snack_bar)
            page.update()

    return ft.Column([
        firstname_input,
        lastname_input,
        date_input,
        ft.Row([
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.ElevatedButton("Save", on_click=handle_submit)
        ], alignment=ft.MainAxisAlignment.END)
    ])


def contacts_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Contacts",
        api_base_url=API_BASE_URL,
        render_item_row=render_contact_row,
        build_edit_form=lambda *args: build_contact_form(*args, page=page),
        build_payload=None
    )
