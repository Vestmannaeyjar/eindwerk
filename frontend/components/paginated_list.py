import flet as ft
import requests
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

import math
from frontend.components.key import GOOGLE_API_KEY


def search_google_places(query):
    """Search for places using Google Places API Text Search"""
    if not query or len(query) < 3:
        return []

    try:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': GOOGLE_API_KEY,
            'fields': 'place_id,name,formatted_address,geometry'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data.get('results', [])[:10]  # Limit to 10 results

    except Exception as e:
        print(f"Error searching Google Places: {e}")
        return []


def get_place_details(place_id):
    """Get detailed information about a place using Place Details API"""
    try:
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'key': GOOGLE_API_KEY,
            'fields': 'name,formatted_address,address_components,geometry,formatted_phone_number,website'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data.get('result', {})

    except Exception as e:
        print(f"Error getting place details: {e}")
        return {}


def parse_address_components(address_components):
    """Parse Google Places address components into structured data"""
    address_data = {
        'street_name': '',
        'street_number': '',
        'city': '',
        'postal_code': '',
        'country': '',
        'province': ''
    }

    for component in address_components:
        types = component.get('types', [])
        long_name = component.get('long_name', '')

        if 'street_number' in types:
            address_data['street_number'] = long_name
        elif 'route' in types:
            address_data['street_name'] = long_name
        elif 'locality' in types:
            address_data['city'] = long_name
        elif 'postal_code' in types:
            address_data['postal_code'] = long_name
        elif 'country' in types:
            address_data['country'] = long_name
        elif 'administrative_area_level_1' in types:
            address_data['province'] = long_name

    return address_data


def create_google_search_dialog(page, on_address_selected, on_cancel, but_color):
    """Create a dialog for searching Google Places"""
    search_input = ft.TextField(
        label="Zoek adres via Google",
        hint_text="Typ een adres, bedrijfsnaam of plaats...",
        autofocus=True,
        expand=True
    )

    search_results = ft.Column(
        controls=[],
        scroll=ft.ScrollMode.AUTO,
        height=300
    )

    search_progress = ft.ProgressRing(visible=False)
    search_error = ft.Text(value="", visible=False, color=ft.Colors.RED)

    def perform_search(e=None):
        query = search_input.value.strip()
        if not query or len(query) < 3:
            search_error.value = "Voer minimaal 3 karakters in om te zoeken"
            search_error.visible = True
            search_results.controls.clear()
            page.update()
            return

        search_error.visible = False
        search_progress.visible = True
        search_results.controls.clear()
        page.update()

        # Perform the search
        places = search_google_places(query)
        search_progress.visible = False

        if not places:
            search_error.value = "Geen resultaten gevonden"
            search_error.visible = True
        else:
            # Display search results
            for place in places:
                place_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(place.get('name', ''), weight=ft.FontWeight.BOLD),
                            ft.Text(place.get('formatted_address', ''), size=12, color=ft.Colors.GREY_700),
                        ]),
                        padding=10,
                        on_click=lambda e, pid=place.get('place_id'): select_place(pid)
                    ),
                    elevation=2
                )
                search_results.controls.append(place_card)

        page.update()

    def select_place(place_id):
        """Handle place selection and get detailed information"""
        search_progress.visible = True
        page.update()

        place_details = get_place_details(place_id)
        search_progress.visible = False

        if place_details:
            # Parse the address components
            address_components = place_details.get('address_components', [])
            parsed_address = parse_address_components(address_components)

            # Create address data object
            address_data = {
                'name': place_details.get('name', ''),
                'street': f"{parsed_address['street_name']} {parsed_address['street_number']}".strip(),
                'city': parsed_address['city'],
                'zip': parsed_address['postal_code'],
                'country': parsed_address['country'],
                'province': parsed_address['province'],
                'phone': place_details.get('formatted_phone_number', ''),
                'website': place_details.get('website', ''),
                'formatted_address': place_details.get('formatted_address', ''),
                'latitude': place_details.get('geometry', {}).get('location', {}).get('lat'),
                'longitude': place_details.get('geometry', {}).get('location', {}).get('lng'),
            }

            # Close the search dialog and pass the data
            page.dialog.open = False
            page.update()
            on_address_selected(address_data)
        else:
            search_error.value = "Fout bij ophalen adresgegevens"
            search_error.visible = True
            page.update()

    # Set up search on enter key and search button
    search_input.on_submit = perform_search

    search_button = ft.ElevatedButton(
        "Zoeken",
        icon=ft.Icons.SEARCH,
        on_click=perform_search,
        color=but_color
    )

    dialog_content = ft.Column([
        ft.Row([search_input, search_button]),
        search_error,
        search_progress,
        ft.Divider(),
        ft.Text("Zoekresultaten:", weight=ft.FontWeight.BOLD),
        search_results,
        ft.Row([
            ft.TextButton("Annuleren", on_click=lambda e: on_cancel()),
        ], alignment=ft.MainAxisAlignment.END)
    ], height=500, width=600)

    return ft.AlertDialog(
        title=ft.Text("Zoek adres via Google"),
        content=dialog_content,
        modal=True
    )


def paginated_list_view(
    page: ft.Page,
    title: str,
    item_description: str,
    api_base_url: str,
    render_item_row,
    build_edit_form,
    build_payload,
    render_header=None,
    p_color=None,
    ab_color=None,
    but_color=None,
):
    container = ft.Column()
    items_column = ft.Column()
    page.scroll = "auto"
    page.title = f"My ticket app / {title}"
    page.appbar.bgcolor = ab_color
    page.bgcolor = p_color

    current_item_id = None
    current_data = {}
    search_term = ""
    next_page_url = None
    prev_page_url = None
    current_page_url = api_base_url

    total_results_text = ft.Text()
    page_status_text = ft.Text()
    search_input = ft.TextField(label=f"Zoek een {item_description}", width=300)

    def update_urls_with_search(url, term=None):
        if not url:
            return None
        parsed = urlparse(url)
        q = parse_qs(parsed.query)

        term = term if term is not None else search_term

        if term:
            q["search"] = [term]
        else:
            q.pop("search", None)

        q_flat = {k: v[0] for k, v in q.items()}
        return urlunparse(parsed._replace(query=urlencode(q_flat)))

    def load_items(url=None):
        nonlocal next_page_url, prev_page_url, current_page_url, render_header
        if not url:
            url = api_base_url
        current_page_url = update_urls_with_search(url)
        items_column.controls.clear()

        if render_header:
            items_column.controls.append(render_header)

        try:
            res = requests.get(current_page_url)
            res.raise_for_status()
            data = res.json()
            items = data.get("results", data)
            total_count = data.get("count", len(items))
            page_size = data.get("page_size", len(items))

            parsed_url = urlparse(current_page_url)
            current_page_num = int(parse_qs(parsed_url.query).get("page", [1])[0])
            total_pages = math.ceil(total_count / page_size)

            total_results_text.value = f"Aantal {title.lower()}: {total_count}"
            page_status_text.value = f"Pagina {current_page_num} van {total_pages}"

            for item in items:
                row = render_item_row(item, open_edit_dialog, delete_item)
                items_column.controls.append(row)

            next_page_url = update_urls_with_search(data.get("next"))
            prev_page_url = update_urls_with_search(data.get("previous"))

            prev_button.disabled = not bool(prev_page_url)
            next_button.disabled = not bool(next_page_url)

        except Exception as e:
            items_column.controls.append(ft.Text(f"Error: {e}", color="red"))

        page.update()

    def on_search(e):
        nonlocal search_term
        search_term = search_input.value.strip()
        load_items(api_base_url)

    def delete_item(item_id):
        def confirm_delete(e):
            try:
                res = requests.delete(f"{api_base_url}{item_id}/")
                res.raise_for_status()
                page.snack_bar = ft.SnackBar(ft.Text(f"{title} verwijderd"))
                delete_dialog.open = False
                load_items()
            except Exception as err:
                page.snack_bar = ft.SnackBar(ft.Text(f"Verwijderen is mislukt: {err}"))
            page.snack_bar.open = True
            page.update()

        delete_dialog.title = ft.Text("Bevestig verwijderen")
        delete_dialog.content = ft.Text("Ben je zeker?")
        delete_dialog.actions = [
            ft.ElevatedButton("Ga terug", on_click=lambda e: close_dialog(), color=ft.Colors.BLUE_500, icon=ft.Icons.ARROW_BACK),
            ft.ElevatedButton("Verwijder", on_click=confirm_delete, color=ft.Colors.RED_500, icon=ft.Icons.DELETE_FOREVER),
        ]
        page.dialog = delete_dialog
        page.open(delete_dialog)
        page.update()

    def close_dialog():
        delete_dialog.open = False
        page.update()

    def open_edit_dialog(item=None):
        nonlocal current_item_id, current_data, item_description
        current_item_id = item["id"] if item else None
        current_data = item or {}
        edit_dialog.content = ft.Container(
            content=build_edit_form(current_data, submit_edit, cancel_edit),
            bgcolor=ft.Colors.WHITE,
        )
        if not current_data:
            edit_dialog.title = f"Maak nieuwe {item_description}"
        else:
            edit_dialog.title = f"Bewerk {item_description}"
        page.dialog = edit_dialog
        page.open(edit_dialog)
        page.update()

    def open_google_edit_dialog(item=None):
        nonlocal current_item_id, current_data, item_description
        current_item_id = item["id"] if item else None
        current_data = item or {}

        # Check if we should show Google search for new addresses
        if not current_data and item_description == "adres":
            # Show Google search dialog first
            def on_address_selected(google_address_data):
                # Merge Google data with current_data and open the regular edit dialog
                current_data.update(google_address_data)
                show_regular_edit_dialog()

            def on_search_cancel():
                # Close dialog and optionally show regular form
                page.dialog.open = False
                page.update()
                # Uncomment next line if you want to show regular form after canceling Google search
                # show_regular_edit_dialog()

            def show_regular_edit_dialog():
                edit_dialog.content = ft.Container(
                    content=build_edit_form(current_data, submit_edit, cancel_edit),
                    bgcolor=ft.Colors.WHITE,
                )
                edit_dialog.title = f"Maak nieuwe {item_description}"
                page.dialog = edit_dialog
                page.open(edit_dialog)
                page.update()

            # Show Google search dialog
            google_dialog = create_google_search_dialog(page, on_address_selected, on_search_cancel, but_color)
            page.dialog = google_dialog
            page.open(google_dialog)
            page.update()

        else:
            # Regular edit dialog for existing items or non-address items
            edit_dialog.content = ft.Container(
                content=build_edit_form(current_data, submit_edit, cancel_edit),
                bgcolor=ft.Colors.WHITE,
            )
            if not current_data:
                edit_dialog.title = f"Maak nieuwe {item_description}"
            else:
                edit_dialog.title = f"Bewerk {item_description}"
            page.dialog = edit_dialog
            page.open(edit_dialog)
            page.update()

    def cancel_edit(e):
        page.close(edit_dialog)
        page.update()

    def submit_edit(payload):
        try:
            if current_item_id:
                res = requests.put(f"{api_base_url}{current_item_id}/", json=payload)
            else:
                res = requests.post(api_base_url, json=payload)
            res.raise_for_status()
            page.snack_bar = ft.SnackBar(ft.Text(f"{title} succesvol bewaard"))
            page.snack_bar.open = True
            page.close(edit_dialog)
            load_items()
        except requests.exceptions.HTTPError as http_err:
            try:
                errors = http_err.response.json()
                error_message = "; ".join(f"{k}: {', '.join(v)}" for k, v in errors.items())
            except:
                error_message = str(http_err)
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {error_message}"))
            page.snack_bar.open = True
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {err}"))
            page.snack_bar.open = True
        page.update()

    prev_button = ft.ElevatedButton("Vorige", on_click=lambda e: load_items(prev_page_url), disabled=True, color=but_color)
    next_button = ft.ElevatedButton("Volgende", on_click=lambda e: load_items(next_page_url), disabled=True, color=but_color)

    search_input.on_change = on_search
    add_button = ft.ElevatedButton(f"Voeg een {item_description} toe", on_click=lambda e: open_edit_dialog(None), icon=ft.Icons.ADD_OUTLINED, color=but_color)
    add_google_button = ft.ElevatedButton(f"Voeg via Google een {item_description} toe", on_click=lambda e: open_google_edit_dialog(None), icon=ft.Icons.ADD_LOCATION_ALT_OUTLINED, color=but_color, visible=(item_description == "adres"))

    edit_dialog = ft.AlertDialog(modal=True, title=ft.Text(f"Bewerk {item_description}"), actions_alignment=ft.MainAxisAlignment.END)
    delete_dialog = ft.AlertDialog(modal=True, actions_alignment=ft.MainAxisAlignment.END)

    top_controls = ft.Row(
        [
            add_button,
            add_google_button,
            search_input,
            prev_button,
            next_button,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        wrap=True,
    )

    container.controls.extend([
        ft.Container(
            content=top_controls,
            expand=True,
            padding=0,
            margin=0,
        ),

        ft.Container(
            content=ft.Row([total_results_text, page_status_text]),
            expand=True,
            padding=0,
            margin=0,
        ),

        # Items list section with white background
        ft.Container(
            content=items_column,
            expand=True,
            padding=0,
            margin=0,
        ),
    ])

    load_items()
    return container
