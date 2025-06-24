import flet as ft
from components.paginated_list import paginated_list_view
from components.dialogcontrol import dialog_controls
from components.error import error_container, show_error
from utilities import render_row, render_task_header

API_BASE_URL = "http://127.0.0.1:8000/api/addresses/"

p_color = ft.Colors.GREEN_50
ab_color = ft.Colors.GREEN_500
but_color = ft.Colors.GREEN_800

ADDRESS_FIELDS = [
    {"key": "name", "label": "Adresnaam", "width": 100},
    {"key": "street", "label": "Straat", "width": 200},
    {"key": "zip", "label": "Postcode", "width": 100},
    {"key": "city", "label": "Plaats", "width": 100},
    {"key": "country", "label": "Land", "width": 100},
]

FIELD_LABELS = {field["key"]: field["label"] for field in ADDRESS_FIELDS}


def render_address_row(address, open_edit_dialog, delete_address, button_color):
    return render_row(address, ADDRESS_FIELDS, open_edit_dialog, delete_address, button_color)


def build_address_form(current_data, on_submit, on_cancel, page):
    name_input = ft.TextField(label=FIELD_LABELS["name"])
    street_input = ft.TextField(label=FIELD_LABELS["street"])
    zip_input = ft.TextField(label=FIELD_LABELS["zip"])
    city_input = ft.TextField(label=FIELD_LABELS["city"])
    country_input = ft.TextField(label=FIELD_LABELS["country"])

    if current_data:
        name_input.value = current_data.get("name", "")
        street_input.value = current_data.get("street", "")
        zip_input.value = current_data.get("zip", "")
        city_input.value = current_data.get("city", "")
        country_input.value = current_data.get("country", "")

    def handle_submit(_):
        try:
            payload = {
                "name": name_input.value.strip(),
                "street": street_input.value.strip(),
                "zip": zip_input.value.strip(),
                "city": city_input.value.strip(),
                "country": country_input.value.strip(),
            }
            on_submit(payload)
        except Exception as e:
            show_error(f"Error: {e}", error_container, page)

    return ft.Column([
        name_input,
        street_input,
        zip_input,
        city_input,
        country_input,
        error_container,
        dialog_controls(on_cancel, handle_submit),
    ])


def addresses_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Adressen",
        item_description="adres",
        api_base_url=API_BASE_URL,
        render_item_row=lambda address, open_edit_dialog, delete_address: render_address_row(
            address, open_edit_dialog, delete_address, but_color),
        build_edit_form=lambda *args: build_address_form(*args, page=page),
        render_header=render_task_header(ADDRESS_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )
