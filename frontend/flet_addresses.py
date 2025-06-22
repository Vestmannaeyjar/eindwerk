import flet as ft
from components.paginated_list import paginated_list_view
from utilities import render_row

API_BASE_URL = "http://127.0.0.1:8000/api/addresses/"

ADDRESS_FIELDS = [
    {"key": "name", "label": "Name", "width": 100},
    {"key": "street", "label": "Street", "width": 100},
    {"key": "zip", "label": "Zip-code", "width": 100},
    {"key": "city", "label": "City", "width": 100},
    {"key": "country", "label": "Country", "width": 100},
]


def render_address_row(address, open_edit_dialog, delete_address):
    return render_row(address, ADDRESS_FIELDS, open_edit_dialog, delete_address)


def build_address_form(current_data, on_submit, on_cancel, page):
    name_input = ft.TextField(label="Name")
    street_input = ft.TextField(label="Street")
    zip_input = ft.TextField(label="Zip")
    city_input = ft.TextField(label="City")
    country_input = ft.TextField(label="Country")

    if current_data:
        name_input.value = current_data.get("name", "")
        street_input.value = current_data.get("street", "")
        zip_input.value = current_data.get("zip", "")
        city_input.value = current_data.get("city", "")
        country_input.value = current_data.get("country", "")

    def handle_submit(e):
        try:
            payload = {
                "name": name_input.value.strip(),
                "street": street_input.value.strip(),
                "zip": zip_input.value.strip(),
                "city": city_input.value.strip(),
                "country": country_input.value.strip(),
            }
            on_submit(payload)
        except Exception as err:
            page.snack_bar.content.value = f"Error: {err}"
            page.open(page.snack_bar)
            page.update()

    return ft.Column([
        name_input,
        street_input,
        zip_input,
        city_input,
        country_input,
        ft.Row([
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.ElevatedButton("Save", on_click=handle_submit)
        ], alignment=ft.MainAxisAlignment.END)
    ])


def addresses_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Adressen",
        item_description="adres",
        api_base_url=API_BASE_URL,
        render_item_row=render_address_row,
        build_edit_form=lambda *args: build_address_form(*args, page=page),
        build_payload=None
    )
