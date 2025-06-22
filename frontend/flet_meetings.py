import flet as ft
from datetime import datetime
import requests
from components.paginated_list import paginated_list_view
from components.datetime_functions import parse_date
from components.dialogcontrol import dialog_controls
from utilities import render_row, render_task_header

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/meetings/"
ROOMS_URL = "http://127.0.0.1:8000/api/tasks/meetingrooms/"
CONTACTS_URL = "http://127.0.0.1:8000/api/contextcontacts/"

p_color = ft.Colors.YELLOW_50
ab_color = ft.Colors.YELLOW_500
but_color = ft.Colors.YELLOW_800

MEETING_FIELDS = [
    {"key": "startdate", "label": "Start", "width": 150, "type": "datetime"},
    {"key": "enddate", "label": "Einde", "width": 150, "type": "datetime"},
    {"key": "name", "label": "Naam", "width": 300},
    {"key": "contacts", "label": "Deelnemers", "width": 200, "display_key": "contextcontact_name"},
    {"key": "meetingroom", "label": "Vergaderzaal", "width": 200, "display_key": "meetingroom_name"},
    {"key": "digital_space", "label": "Digitale ruimte (URL)", "width": 200},
]

FIELD_LABELS = {field["key"]: field["label"] for field in MEETING_FIELDS}


def format_datetime_for_api(dt):
    """Format datetime object to API-expected format with Z suffix."""
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_datetime_input(date_str):
    """Parse datetime input with multiple format support"""
    if not date_str or not date_str.strip():
        return None

    date_str = date_str.strip()

    # Common datetime formats to try
    formats = [
        "%d-%m-%Y %H:%M",  # dd-mm-yyyy hh:mm
        "%d-%m-%Y",  # dd-mm-yyyy (will add 00:00 time)
        "%Y-%m-%d %H:%M:%S",  # yyyy-mm-dd hh:mm:ss
        "%Y-%m-%d %H:%M",  # yyyy-mm-dd hh:mm
        "%Y-%m-%d",  # yyyy-mm-dd
        "%d/%m/%Y %H:%M",  # dd/mm/yyyy hh:mm
        "%d/%m/%Y",  # dd/mm/yyyy
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            print(f"Successfully parsed '{date_str}' with format '{fmt}' -> {dt}")
            return dt
        except ValueError:
            continue

    print(f"Failed to parse date: '{date_str}'")
    return None


def render_meeting_row(meeting, open_edit_dialog, delete_meeting, but_color):
    return render_row(meeting, MEETING_FIELDS, open_edit_dialog, delete_meeting, but_color)


def build_meeting_form(current_data, on_submit, on_cancel, page):
    title_input = ft.TextField(label=FIELD_LABELS["name"])
    startdate_input = ft.TextField(label=FIELD_LABELS["startdate"])
    enddate_input = ft.TextField(label=FIELD_LABELS["enddate"])
    digital_space_input = ft.TextField(label=FIELD_LABELS["digital_space"])
    room_dropdown = ft.Dropdown(label=FIELD_LABELS["meetingroom"])
    error_text = ft.Text(
        value="",
        visible=False,
        size=14,
        color=ft.Colors.RED,
    )

    selected_contacts = []
    selected_contacts_display = ft.Column()

    # Dropdown for available contacts - Initialize with empty options
    contacts_dropdown = ft.Dropdown(
        label="Selecteer deelnemer",
        hint_text="Kies een deelnemer om toe te voegen",
        options=[],  # Start with empty options
        on_change=None  # Will be set below
    )

    def load_contacts():
        """Load available contacts from API"""
        try:
            print("Loading contacts...")  # Debug print

            # Load all contacts from paginated API
            all_contacts = []
            next_url = CONTACTS_URL

            while next_url:
                res = requests.get(next_url)
                res.raise_for_status()
                data = res.json()

                contacts = data.get("results", [])
                all_contacts.extend(contacts)

                # Get next page URL
                next_url = data.get("next")
                print(f"Loaded {len(contacts)} contacts from current page, total: {len(all_contacts)}")

            print(f"Loaded {len(all_contacts)} total contacts")  # Debug print

            # Create dropdown options using firstname and lastname
            contacts_dropdown.options = []
            for contact in all_contacts:
                contact_id = contact.get("id")
                if contact_id is None:
                    continue

                contact_name = contact.get("contextcontact_name", "").strip()

                contacts_dropdown.options.append(
                    ft.dropdown.Option(str(contact_id), contact_name)
                )

            # Sort contacts by name for better UX
            contacts_dropdown.options.sort(key=lambda x: x.text)

            print(f"Created {len(contacts_dropdown.options)} dropdown options")  # Debug print
            page.update()

        except requests.exceptions.RequestException as e:
            print(f"Network error loading contacts: {e}")
            error_text.value = f"Fout bij laden contacten: {e}"
            error_text.visible = True
            page.update()
        except Exception as e:
            print(f"Error loading contacts: {e}")
            error_text.value = f"Fout bij laden contacten: {e}"
            error_text.visible = True
            page.update()

    def load_meeting_rooms():
        try:
            print("Loading meeting rooms...")  # Debug print
            res = requests.get(ROOMS_URL)
            res.raise_for_status()
            data = res.json()
            rooms = data.get("results", data)

            # Ensure rooms is a list
            if not isinstance(rooms, list):
                rooms = []

            room_dropdown.options = [
                ft.dropdown.Option(str(r["id"]), r["name"])
                for r in rooms
                if "id" in r and "name" in r  # Safety check
            ]
            print(f"Loaded {len(room_dropdown.options)} meeting rooms")  # Debug print
            page.update()

        except requests.exceptions.RequestException as e:
            print(f"Network error loading meeting rooms: {e}")
        except Exception as e:
            print(f"Error loading meeting rooms: {e}")

    def add_contact(e):
        """Add selected contact to the meeting"""
        if contacts_dropdown.value:
            contact_id = contacts_dropdown.value
            # Find the contact name from the dropdown options
            contact_name = None
            for option in contacts_dropdown.options:
                if option.key == contact_id:
                    contact_name = option.text
                    break

            # Check if contact is already added
            if contact_id not in [c["id"] for c in selected_contacts]:
                selected_contacts.append({
                    "id": contact_id,
                    "name": contact_name or f"Contact {contact_id}"
                })
                update_contacts_display()

            # Clear the dropdown selection
            contacts_dropdown.value = None
            page.update()

    def remove_contact(contact_id):
        """Remove a contact from the selected contacts"""
        nonlocal selected_contacts  # Use nonlocal instead of global
        selected_contacts = [c for c in selected_contacts if c["id"] != contact_id]
        update_contacts_display()

    def update_contacts_display():
        """Update the display of selected contacts"""
        selected_contacts_display.controls.clear()

        if selected_contacts:
            selected_contacts_display.controls.append(
                ft.Text("Geselecteerde deelnemers:", weight=ft.FontWeight.BOLD)
            )

            for contact in selected_contacts:
                selected_contacts_display.controls.append(
                    ft.Row([
                        ft.Text(contact["name"]),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=ft.Colors.RED,
                            icon_size=16,
                            on_click=lambda e, cid=contact["id"]: remove_contact(cid),
                            tooltip="Verwijder deelnemer"
                        )
                    ])
                )
        else:
            selected_contacts_display.controls.append(
                ft.Text("Geen deelnemers geselecteerd", italic=True, color=ft.Colors.GREY)
            )

        page.update()

    # Set the on_change handler for contacts dropdown
    contacts_dropdown.on_change = add_contact

    # Load data after setting up all handlers
    load_meeting_rooms()
    load_contacts()

    if current_data:
        title_input.value = current_data.get("name", "")

        s_date_str = current_data.get("startdate", "")
        e_date_str = current_data.get("enddate", "")

        # Fix: Add null checks before parsing datetime
        if s_date_str:  # Only parse if not None/empty
            try:
                s_dt = datetime.strptime(s_date_str, "%Y-%m-%dT%H:%M:%SZ")
                startdate_input.value = s_dt.strftime("%d-%m-%Y %H:%M")
            except (ValueError, TypeError) as e:
                print(f"Error parsing startdate '{s_date_str}': {e}")
                startdate_input.value = s_date_str if s_date_str else ""
        else:
            startdate_input.value = ""

        if e_date_str:  # Only parse if not None/empty
            try:
                e_dt = datetime.strptime(e_date_str, "%Y-%m-%dT%H:%M:%SZ")
                enddate_input.value = e_dt.strftime("%d-%m-%Y %H:%M")
            except (ValueError, TypeError) as e:
                print(f"Error parsing enddate '{e_date_str}': {e}")
                enddate_input.value = e_date_str if e_date_str else ""
        else:
            enddate_input.value = ""

        digital_space_input.value = current_data.get("digital_space", "")
        room_dropdown.value = str(current_data.get("meetingroom", "")) if current_data.get("meetingroom") else None

        # Load existing contacts
        existing_contacts = current_data.get("contacts", [])
        if existing_contacts:
            # If contacts are provided as a list of IDs or objects
            for contact in existing_contacts:
                if isinstance(contact, dict):
                    contact_id = str(contact.get("id", contact.get("contact_id", "")))
                    # Handle firstname/lastname combination
                    firstname = contact.get("firstname", "")
                    lastname = contact.get("lastname", "")
                    if firstname and lastname:
                        contact_name = f"{firstname} {lastname}"
                    elif firstname:
                        contact_name = firstname
                    elif lastname:
                        contact_name = lastname
                    else:
                        contact_name = contact.get("name", f"Contact {contact_id}")

                    selected_contacts.append({
                        "id": contact_id,
                        "name": contact_name
                    })
                else:
                    # If it's just an ID, you might need to fetch the name
                    selected_contacts.append({
                        "id": str(contact),
                        "name": f"Contact {contact}"  # You might want to fetch the actual name
                    })

    # Initialize contacts display
    update_contacts_display()

    def validate_form_data():
        """Validate form inputs and return cleaned data."""
        # Validate subject
        name = title_input.value.strip() if title_input.value else ""
        if not name:
            raise ValueError("Naam is verplicht.")

        # Parse dates - debug the input values
        startdate_str = startdate_input.value.strip() if startdate_input.value else ""
        enddate_str = enddate_input.value.strip() if enddate_input.value else ""

        print(f"Date inputs - Start: '{startdate_str}', End: '{enddate_str}'")

        if not startdate_str:
            raise ValueError("Startdatum is verplicht.")
        if not enddate_str:
            raise ValueError("Einddatum is verplicht.")

        # Parse dates - handle both string and datetime returns
        startdate_parsed = parse_date(startdate_str) or parse_datetime_input(startdate_str)
        enddate_parsed = parse_date(enddate_str) or parse_datetime_input(enddate_str)

        print(f"Parsed dates - Start: {startdate_parsed}, End: {enddate_parsed}")

        # Convert to datetime objects if they're strings
        if isinstance(startdate_parsed, str):
            try:
                # If parse_date returned ISO string, parse it back to datetime
                startdate = datetime.fromisoformat(startdate_parsed.replace('Z', '+00:00'))
            except ValueError:
                startdate = None
        else:
            startdate = startdate_parsed

        if isinstance(enddate_parsed, str):
            try:
                # If parse_date returned ISO string, parse it back to datetime
                enddate = datetime.fromisoformat(enddate_parsed.replace('Z', '+00:00'))
            except ValueError:
                enddate = None
        else:
            enddate = enddate_parsed

        print(f"Final datetime objects - Start: {startdate}, End: {enddate}")

        if startdate is None:
            raise ValueError("Startdatum heeft een ongeldig formaat. Gebruik: dd-mm-yyyy hh:mm")
        if enddate is None:
            raise ValueError("Einddatum heeft een ongeldig formaat. Gebruik: dd-mm-yyyy hh:mm")

        if enddate <= startdate:
            raise ValueError("Einddatum moet na startdatum zijn.")

        digital_space = digital_space_input.value.strip() if digital_space_input.value else ""

        # Convert meetingroom to integer if it exists
        meetingroom_id = None
        if room_dropdown.value:
            try:
                meetingroom_id = int(room_dropdown.value)
            except ValueError:
                raise ValueError("Ongeldig vergaderzaal ID.")

        # Convert contact IDs to integers
        contact_ids = []
        for contact in selected_contacts:
            try:
                contact_ids.append(int(contact["id"]))
            except ValueError:
                raise ValueError(f"Ongeldig contact ID: {contact['id']}")

        payload = {
            "name": name,
            "startdate": format_datetime_for_api(startdate),
            "enddate": format_datetime_for_api(enddate),
            "contacts": contact_ids,
            "digital_space": digital_space,
            "meetingroom": meetingroom_id,
        }

        # Debug: Print the payload being sent
        print(f"Payload being sent to API: {payload}")

        return payload

    def show_error(message):
        """Show error message in the form."""
        error_text.value = message
        error_text.visible = True
        page.update()

    def hide_error():
        """Hide error message."""
        error_text.visible = False
        page.update()

    def handle_submit(e):
        hide_error()

        try:
            payload = validate_form_data()
            print(f"Submitting payload: {payload}")  # Debug print
            on_submit(payload)
        except ValueError as validation_err:
            print(f"Validation error: {validation_err}")
            show_error(str(validation_err))
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
            try:
                # Try to get the detailed error response
                error_detail = http_err.response.json()
                print(f"API error details: {error_detail}")
                show_error(f"API fout: {error_detail}")
            except:
                show_error(f"HTTP fout: {http_err}")
        except Exception as err:
            print(f"General error: {err}")
            show_error(f"Fout bij opslaan: {err}")

    return ft.Column([
        title_input,
        startdate_input,
        enddate_input,
        digital_space_input,
        room_dropdown,
        ft.Divider(),
        ft.Text("Deelnemers", size=16, weight=ft.FontWeight.BOLD),
        contacts_dropdown,
        selected_contacts_display,
        error_text,
        dialog_controls(on_cancel, handle_submit, but_color),
    ])


def meetings_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Vergaderingen",
        item_description="vergadering",
        api_base_url=API_BASE_URL,
        render_item_row=lambda meeting, open_edit_dialog, delete_meeting: render_meeting_row(
            meeting, open_edit_dialog, delete_meeting, but_color),
        build_edit_form=lambda *args: build_meeting_form(*args, page=page),
        build_payload=None,
        render_header=render_task_header(MEETING_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )