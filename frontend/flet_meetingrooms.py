import flet as ft
import requests
from components.paginated_list import paginated_list_view
from components.dialogcontrol import dialog_controls
from components.error import error_container, show_error, hide_error
from utilities import render_row, render_task_header

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/meetingrooms/"

p_color = ft.Colors.PURPLE_50
ab_color = ft.Colors.PURPLE_500
but_color = ft.Colors.PURPLE_800

MEETINGROOM_FIELDS = [
    {"key": "name", "label": "Naam", "width": 400},
    {"key": "capacity", "label": "Capaciteit", "width": 100},
]

FIELD_LABELS = {field["key"]: field["label"] for field in MEETINGROOM_FIELDS}


def render_meetingroom_row(meetingroom, open_edit_dialog, delete_meetingroom, button_color):
    return render_row(meetingroom, MEETINGROOM_FIELDS, open_edit_dialog, delete_meetingroom, button_color)


def build_meetingroom_form(current_data, on_submit, on_cancel, page):
    name_input = ft.TextField(label=FIELD_LABELS["name"])
    capacity_input = ft.TextField(label=FIELD_LABELS["capacity"])

    if current_data:
        name_input.value = current_data.get("name", "")
        capacity_input.value = current_data.get("capacity", "")

    def handle_submit(_):
        hide_error(error_container, page)
        try:
            payload = {
                "name": name_input.value.strip(),
                "capacity": capacity_input.value,
            }
            on_submit(payload)
        except requests.exceptions.HTTPError as err:
            # Attempt to parse JSON error response
            try:
                error_data = err.response.json()  # This is the key part
                error_messages = []
                for field, messages in error_data.items():
                    if isinstance(messages, list):
                        for msg in messages:
                            error_messages.append(f"{field}: {msg}")
                    else:
                        error_messages.append(f"{field}: {messages}")
                show_error(" • " + "\n • ".join(error_messages), error_container, page)
                print("test")
            except Exception:
                # Fallback if the response isn't JSON or something goes wrong
                show_error(f"HTTP Error: {err}", error_container, page)
        except Exception as err:
            # Handle any other errors
            show_error(f"Error: {err}", error_container, page)

    return ft.Column([
        name_input,
        capacity_input,
        error_container,
        dialog_controls(on_cancel, handle_submit),
    ])


def meetingrooms_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Vergaderzalen",
        item_description="vergaderzaal",
        api_base_url=API_BASE_URL,
        render_item_row=lambda meetingroom, open_edit_dialog, delete_meetingroom: render_meetingroom_row(
            meetingroom, open_edit_dialog, delete_meetingroom, but_color),
        build_edit_form=lambda *args: build_meetingroom_form(*args, page=page),
        render_header=render_task_header(MEETINGROOM_FIELDS),
        p_color=p_color,
        ab_color=ab_color,
        but_color=but_color,
    )
