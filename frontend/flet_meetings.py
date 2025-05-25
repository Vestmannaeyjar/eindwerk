import flet as ft
from datetime import datetime
import requests
from components.paginated_list import paginated_list_view

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/meetings/"
ROOMS_URL = "http://127.0.0.1:8000/api/tasks/meetingrooms/"


def render_meeting_row(meeting, open_edit_dialog, delete_meeting):
    return ft.Row([
        ft.Text(f"{meeting['name']} – {meeting['date']} – {meeting['digital_space']}", expand=True),
        ft.IconButton(icon="edit", tooltip="Edit", on_click=lambda e: open_edit_dialog(meeting)),
        ft.IconButton(icon="delete", tooltip="Delete", on_click=lambda e: delete_meeting(meeting["id"])),
    ])


def build_meeting_form(current_data, on_submit, on_cancel, page):
    title_input = ft.TextField(label="Title")
    date_input = ft.TextField(label="Date (dd-mm-yyyy)")
    digital_space_input = ft.TextField(label="Digital Space")
    room_dropdown = ft.Dropdown(label="Meeting Room")

    def load_meeting_rooms():
        try:
            res = requests.get(ROOMS_URL)
            res.raise_for_status()
            data = res.json()
            rooms = data.get("results", data)
            room_dropdown.options = [ft.dropdown.Option(str(r["id"]), r["name"]) for r in rooms]
        except Exception as e:
            print("Error loading rooms:", e)

    load_meeting_rooms()

    if current_data:
        title_input.value = current_data.get("name", "")
        date_str = current_data.get("date", "")
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            date_input.value = dt.strftime("%d-%m-%Y")
        except:
            date_input.value = date_str
        digital_space_input.value = current_data.get("digital_space", "")
        room_dropdown.value = str(current_data.get("meetingroom", ""))

    def handle_submit(e):
        try:
            if not room_dropdown.value:
                raise ValueError("Meeting room is required.")
            dt = datetime.strptime(date_input.value, "%d-%m-%Y")
            iso_date = dt.isoformat() + "Z"

            payload = {
                "name": title_input.value.strip(),
                "date": iso_date,
                "digital_space": digital_space_input.value.strip(),
                "meetingroom": int(room_dropdown.value)
            }
            on_submit(payload)
        except Exception as err:
            page.snack_bar.content.value = f"Error: {err}"
            page.open(page.snack_bar)
            page.update()

    return ft.Column([
        title_input,
        date_input,
        digital_space_input,
        room_dropdown,
        ft.Row([
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.ElevatedButton("Save", on_click=handle_submit)
        ], alignment=ft.MainAxisAlignment.END)
    ])


def meetings_view(page: ft.Page):
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    return paginated_list_view(
        page=page,
        title="Meetings",
        api_base_url=API_BASE_URL,
        render_item_row=render_meeting_row,
        build_edit_form=lambda *args: build_meeting_form(*args, page=page),
        build_payload=None
    )
