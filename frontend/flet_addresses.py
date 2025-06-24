import flet as ft
from components.paginated_list import paginated_list_view
from components.dialogcontrol import dialog_controls
from components.error import error_container, show_error, hide_error
from utilities import render_row, render_task_header
import urllib.parse

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


def create_google_maps_url(address):
    """Create a Google Maps URL from address components"""
    address_parts = []

    if address.get("street"):
        address_parts.append(address["street"])
    if address.get("zip"):
        address_parts.append(address["zip"])
    if address.get("city"):
        address_parts.append(address["city"])
    if address.get("country"):
        address_parts.append(address["country"])

    if not address_parts:
        return None

    address_string = ", ".join(address_parts)
    encoded_address = urllib.parse.quote(address_string)
    return f"https://www.google.com/maps/search/?api=1&query={encoded_address}"


def show_map_popup(page, address):
    """Show a popup with Google Maps embedded view"""
    maps_url = create_google_maps_url(address)

    if not maps_url:
        page.snack_bar.content.value = "Geen adresgegevens beschikbaar voor kaart"
        page.snack_bar.open = True
        page.update()
        return

    # Create embedded map URL
    embed_url = maps_url.replace("search/?api=1&query=", "embed?q=")

    # Create the map dialog
    map_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Locatie: {address.get('name', 'Onbekend')}"),
        content=ft.Container(
            content=ft.Column([
                ft.Text(f"Adres: {format_address_string(address)}", size=14),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton(
                            "Open in Google Maps",
                            icon=ft.Icons.OPEN_IN_NEW,
                            on_click=lambda _: page.launch_url(maps_url)
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    margin=ft.margin.only(top=10)
                )
            ]),
            width=400,
            height=200
        ),
        actions=[
            ft.TextButton("Sluiten", on_click=lambda _: close_dialog(page, map_dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(map_dialog)
    map_dialog.open = True
    page.update()


def close_dialog(page, dialog):
    """Close and remove dialog"""
    dialog.open = False
    page.update()
    page.overlay.remove(dialog)


def format_address_string(address):
    """Format address into a readable string"""
    parts = []
    if address.get("street"):
        parts.append(address["street"])
    if address.get("zip") or address.get("city"):
        city_part = []
        if address.get("zip"):
            city_part.append(address["zip"])
        if address.get("city"):
            city_part.append(address["city"])
        parts.append(" ".join(city_part))
    if address.get("country"):
        parts.append(address["country"])

    return ", ".join(parts) if parts else "Geen adres beschikbaar"


def has_mappable_address(address):
    """Check if address has enough info to be mapped"""
    return bool(address.get("street") or address.get("city"))


def render_address_row(address, open_edit_dialog, delete_address, button_color, page):
    """Enhanced render function with map icon"""
    # Get the base row from the original render_row function
    base_row = render_row(address, ADDRESS_FIELDS, open_edit_dialog, delete_address, button_color)

    # Create map button if address is mappable
    map_button = None
    if has_mappable_address(address):
        map_button = ft.IconButton(
            icon=ft.Icons.MAP,
            tooltip="Toon op kaart",
            icon_color=ft.Colors.BLUE_600,
            on_click=lambda _: show_map_popup(page, address)
        )
    else:
        # Placeholder to maintain alignment
        map_button = ft.Container(width=40, height=40)

    # If base_row is a Row, add the map button to its controls
    if isinstance(base_row, ft.Row):
        base_row.controls.append(map_button)
    else:
        # If it's not a Row, wrap it in a Row with the map button
        base_row = ft.Row([
            base_row,
            map_button
        ])

    return base_row


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
        hide_error(error_container, page)
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
            address, open_edit_dialog, delete_address, but_color, page),
        build_edit_form=lambda *args: build_address_form(*args, page=page),
        render_header=render_task_header(ADDRESS_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )