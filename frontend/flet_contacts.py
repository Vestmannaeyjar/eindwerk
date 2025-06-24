import flet as ft
import requests
from datetime import datetime
from components.paginated_list import paginated_list_view
from components.dialogcontrol import dialog_controls
from components.error import error_container, show_error, hide_error
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


def render_contact_row(contact, open_edit_dialog, delete_contact, button_color, show_context_contacts):
    """Enhanced contact row with context contacts button"""
    # Create the base row using your existing render_row function
    base_row = render_row(contact, CONTACT_FIELDS, open_edit_dialog, delete_contact, button_color)

    # Add context contacts button
    context_btn = ft.IconButton(
        icon=ft.Icons.PEOPLE,
        tooltip="Context contacten",
        on_click=lambda _: show_context_contacts(contact),
        icon_color=button_color,
    )

    # Add the button to the row's controls
    if hasattr(base_row, 'controls') and isinstance(base_row.controls[-1], ft.Row):
        # If the last control is a Row (button container), add to it
        base_row.controls[-1].controls.append(context_btn)
    else:
        # Otherwise, create a new button container
        button_container = ft.Row([context_btn], alignment=ft.MainAxisAlignment.END)
        base_row.controls.append(button_container)

    return base_row


def fetch_context_contacts(contact_id):
    """Fetch context contacts for a specific contact from the API"""
    try:
        # Fetch context contacts using the custom action endpoint
        response = requests.get(f"http://127.0.0.1:8000/api/contacts/{contact_id}/context_contacts/")
        if response.status_code == 200:
            return response.json()  # Direct array response from custom action
        else:
            print(f"API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching context contacts: {e}")
        return []


def create_context_contact(contact_id, context_data):
    """Create a new context contact via API"""
    try:
        payload = {
            "contact": contact_id,
            "context": context_data["context"],
            "function": context_data["function"],
            "emailaddress": context_data["emailaddress"],
            "telephone": context_data["telephone"],
            "parking_info": context_data["parking_info"],
            "postaladdress": context_data.get("postaladdress", 1)  # Default address ID
        }
        response = requests.post("http://127.0.0.1:8000/api/contextcontacts/", json=payload)
        if response.status_code == 201:
            return True, "Context contact succesvol toegevoegd!"
        else:
            return False, f"API Error: {response.status_code}"
    except Exception as e:
        return False, f"Error creating context contact: {e}"


def update_context_contact(context_contact_id, context_data):
    """Update an existing context contact via API"""
    try:
        payload = {
            "context": context_data["context"],
            "function": context_data["function"],
            "emailaddress": context_data["emailaddress"],
            "telephone": context_data["telephone"],
            "parking_info": context_data["parking_info"],
            "postaladdress": context_data.get("postaladdress", 1)
        }
        response = requests.put(f"http://127.0.0.1:8000/api/contextcontacts/{context_contact_id}/", json=payload)
        if response.status_code == 200:
            return True, "Context contact succesvol bijgewerkt!"
        else:
            return False, f"API Error: {response.status_code}"
    except Exception as e:
        return False, f"Error updating context contact: {e}"


def build_add_context_form(contact, on_submit, on_cancel, page, context_contact=None):
    """Build form for adding a new context contact or editing an existing one"""
    is_edit = context_contact is not None

    inputs = {
        "context": ft.TextField(
            label="Context",
            hint_text="bijv. werk, thuis, school",
            value=context_contact.get("context", "") if is_edit else ""
        ),
        "function": ft.TextField(
            label="Functie",
            hint_text="bijv. manager, huurder, student",
            value=context_contact.get("function", "") if is_edit else ""
        ),
        "emailaddress": ft.TextField(
            label="Email adres",
            value=context_contact.get("emailaddress", "") if is_edit else ""
        ),
        "telephone": ft.TextField(
            label="Telefoon",
            value=context_contact.get("telephone", "") if is_edit else ""
        ),
        "parking_info": ft.TextField(
            label="Parking info",
            multiline=True,
            min_lines=2,
            max_lines=4,
            hint_text="Parking informatie en instructies",
            value=context_contact.get("parking_info", "") if is_edit else ""
        ),
    }

    error_container_form = ft.Container(visible=False)

    def handle_submit(_):
        hide_error(error_container, page)
        try:
            # Validate required fields
            if not inputs["context"].value or not inputs["function"].value:
                error_container_form.content = ft.Text(
                    "Context en Functie zijn verplichte velden",
                    color=ft.Colors.RED
                )
                error_container_form.visible = True
                page.update()
                return

            context_data = {
                "context": inputs["context"].value.strip(),
                "function": inputs["function"].value.strip(),
                "emailaddress": inputs["emailaddress"].value.strip() or "",
                "telephone": inputs["telephone"].value.strip() or "",
                "parking_info": inputs["parking_info"].value.strip() or "",
            }

            if is_edit:
                success, message = update_context_contact(context_contact["id"], context_data)
            else:
                success, message = create_context_contact(contact["id"], context_data)

            if success:
                on_submit()  # Close form and refresh
            else:
                error_container_form.content = ft.Text(message, color=ft.Colors.RED)
                error_container_form.visible = True
                page.update()

        except Exception as e:
            error_container_form.content = ft.Text(f"Error: {e}", color=ft.Colors.RED)
            error_container_form.visible = True
            page.update()

    title_text = f"{'Bewerk' if is_edit else 'Nieuwe'} context contact voor {contact.get('firstname', '')} {contact.get('lastname', '')}"
    button_text = "Bijwerken" if is_edit else "Toevoegen"

    return ft.Column([
        ft.Text(
            title_text,
            size=16,
            weight=ft.FontWeight.BOLD
        ),
        ft.Divider(),
        *inputs.values(),
        error_container_form,
        ft.Row([
            ft.TextButton("Annuleren", on_click=lambda _: on_cancel()),
            ft.ElevatedButton(button_text, on_click=handle_submit),
        ], alignment=ft.MainAxisAlignment.END)
    ])


def build_context_contacts_dialog(contact, page):
    """Build dialog showing context contacts for a specific contact"""
    context_contacts = fetch_context_contacts(contact.get("id"))

    dialog_title = ft.Text(
        f"Context contacten voor {contact.get('firstname', '')} {contact.get('lastname', '')}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # State for showing add form
    show_add_form = ft.Ref[bool]()
    show_add_form.current = False
    edit_context_contact = ft.Ref()
    edit_context_contact.current = None

    def refresh_dialog():
        """Refresh the dialog content"""
        nonlocal dialog
        dialog.open = False
        page.update()
        # Reopen with fresh data
        show_context_contacts_dialog(contact, page)

    def toggle_add_form():
        """Toggle between list view and add form"""
        show_add_form.current = not show_add_form.current
        edit_context_contact.current = None
        update_dialog_content()

    def edit_context_contact_form(ctx_contact):
        """Show edit form for a specific context contact"""
        show_add_form.current = True
        edit_context_contact.current = ctx_contact
        update_dialog_content()

    def update_dialog_content():
        """Update dialog content based on current state"""
        if show_add_form.current:
            # Show add/edit form
            dialog.content = build_add_context_form(
                contact,
                refresh_dialog,  # on_submit
                toggle_add_form,  # on_cancel
                page,
                edit_context_contact.current  # context_contact for editing
            )
            dialog.actions = []  # Remove default actions when showing form
        else:
            # Show context contacts list
            updated_context_contacts = fetch_context_contacts(contact.get("id"))

            if not updated_context_contacts:
                content = ft.Column([
                    dialog_title,
                    ft.Divider(),
                    ft.Text("Geen context contacten gevonden.", italic=True),
                ])
            else:
                # Create list of context contacts
                context_list = []
                for ctx_contact in updated_context_contacts:
                    # Create a card for each context contact with all details
                    card_content = ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.WORK, color=but_color),
                            ft.Text(
                                ctx_contact.get('context', 'Onbekende context'),
                                weight=ft.FontWeight.BOLD,
                                size=14
                            ),
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Bewerken",
                                    icon_color=but_color,
                                    icon_size=16,
                                    on_click=lambda _, ctx=ctx_contact: edit_context_contact_form(ctx)
                                )
                            ], alignment=ft.MainAxisAlignment.END)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(f"Functie: {ctx_contact.get('function', 'Niet gespecificeerd')}", size=12),
                        ft.Text(f"Email: {ctx_contact.get('emailaddress', 'Niet beschikbaar')}", size=12),
                        ft.Text(f"Telefoon: {ctx_contact.get('telephone', 'Niet beschikbaar')}", size=12),
                        ft.Text(
                            f"Parking: {ctx_contact.get('parking_info', 'Geen info')}",
                            size=12,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS
                        ) if ctx_contact.get('parking_info') else None,
                    ])

                    # Filter out None values
                    card_content.controls = [ctrl for ctrl in card_content.controls if ctrl is not None]

                    context_card = ft.Card(
                        content=ft.Container(
                            content=card_content,
                            padding=10,
                        ),
                        margin=ft.margin.only(bottom=8),
                    )

                    context_list.append(context_card)

                content = ft.Column([
                    dialog_title,
                    ft.Divider(),
                    ft.Container(
                        content=ft.Column(context_list, scroll=ft.ScrollMode.AUTO),
                        height=min(500, len(context_list) * 120 + 50),  # Dynamic height with max
                        padding=10,
                    )
                ])

            dialog.content = content
            dialog.actions = [
                ft.TextButton("Toevoegen", on_click=lambda _: toggle_add_form()),
                ft.TextButton("Sluiten", on_click=lambda _: close_dialog(dialog, page))
            ]

        page.update()

    # Initial content
    if not context_contacts:
        content = ft.Column([
            dialog_title,
            ft.Divider(),
            ft.Text("Geen context contacten gevonden.", italic=True),
        ])
    else:
        # Create list of context contacts
        context_list = []
        for ctx_contact in context_contacts:
            # Create a card for each context contact with all details
            card_content = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.WORK, color=but_color),
                    ft.Text(
                        ctx_contact.get('context', 'Onbekende context'),
                        weight=ft.FontWeight.BOLD,
                        size=14
                    ),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Bewerken",
                            icon_color=but_color,
                            icon_size=16,
                            on_click=lambda _, ctx=ctx_contact: edit_context_contact_form(ctx)
                        )
                    ], alignment=ft.MainAxisAlignment.END)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(f"Functie: {ctx_contact.get('function', 'Niet gespecificeerd')}", size=12),
                ft.Text(f"Email: {ctx_contact.get('emailaddress', 'Niet beschikbaar')}", size=12),
                ft.Text(f"Telefoon: {ctx_contact.get('telephone', 'Niet beschikbaar')}", size=12),
                ft.Text(
                    f"Parking: {ctx_contact.get('parking_info', 'Geen info')}",
                    size=12,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ) if ctx_contact.get('parking_info') else None,
            ])

            # Filter out None values
            card_content.controls = [ctrl for ctrl in card_content.controls if ctrl is not None]

            context_card = ft.Card(
                content=ft.Container(
                    content=card_content,
                    padding=10,
                ),
                margin=ft.margin.only(bottom=8),
            )

            context_list.append(context_card)

        content = ft.Column([
            dialog_title,
            ft.Divider(),
            ft.Container(
                content=ft.Column(context_list, scroll=ft.ScrollMode.AUTO),
                height=min(500, len(context_list) * 120 + 50),  # Dynamic height with max
                padding=10,
            )
        ])

    dialog = ft.AlertDialog(
        title=ft.Text("Context Contacten"),
        content=content,
        actions=[
            ft.TextButton("Toevoegen", on_click=lambda _: toggle_add_form()),
            ft.TextButton("Sluiten", on_click=lambda _: close_dialog(dialog, page))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Store the update function in the dialog for access
    dialog.update_content = update_dialog_content

    return dialog


def close_dialog(dialog, page):
    """Close the dialog"""
    dialog.open = False
    page.update()


def show_context_contacts_dialog(contact, page):
    """Show the context contacts dialog"""
    dialog = build_context_contacts_dialog(contact, page)
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def build_contact_form(current_data, on_submit, on_cancel, page):
    inputs = {}
    for field in CONTACT_FIELDS:
        key = field["key"]
        inputs[key] = ft.TextField(label=field["label"])
        if current_data and key in current_data:
            value = current_data[key]
            if key == "date_of_birth":
                value = datetime.strptime(value, "%Y-%m-%d").strftime("%d-%m-%Y")
            inputs[key].value = value

    def handle_submit(_):
        hide_error(error_container, page)
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
        dialog_controls(on_cancel, handle_submit),
    ])


def contacts_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Personen",
        item_description="persoon",
        api_base_url=API_BASE_URL,
        render_item_row=lambda contact, open_edit_dialog, delete_contact: render_contact_row(
            contact,
            open_edit_dialog,
            delete_contact,
            but_color,
            lambda c: show_context_contacts_dialog(c, page)  # Pass the show_context_contacts function
        ),
        build_edit_form=lambda *args: build_contact_form(*args, page=page),
        render_header=render_task_header(CONTACT_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )