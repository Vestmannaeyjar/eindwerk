import flet as ft
from datetime import datetime


def render_row(data, fields, edit_cb, delete_cb):
    def get_display_value(field, data):
        """Get the display value for a field."""
        key = field["key"]

        # Check if field has a custom display key (for foreign keys)
        if "display_key" in field:
            value = str(data.get(field["display_key"], ""))
        else:
            value = data.get(key, "")

        # Format datetime fields
        if field.get("type") == "datetime" and value:
            try:
                # Parse ISO datetime string
                dt = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
                return dt.strftime("%d-%m-%Y %H:%M")
            except (ValueError, AttributeError):
                return str(value)  # Return original if parsing fails

        return str(value) if value else ""

    return ft.Row([
        *[
            ft.Container(content=ft.Text(get_display_value(f, data)), width=f["width"])
            for f in fields
        ],
        ft.IconButton(icon="edit", tooltip="Edit", on_click=lambda e: edit_cb(data)),
        ft.IconButton(icon="delete", tooltip="Delete", on_click=lambda e: delete_cb(data["id"])),
    ])


def render_task_header(fields):
    """Render the header row for task list"""
    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text(
                    field["label"],
                    weight=ft.FontWeight.BOLD,
                    size=14
                ),
                width=field["width"],
                padding=ft.padding.symmetric(horizontal=8, vertical=4)
            )
            for field in fields
        ]),
        bgcolor=ft.Colors.GREY_100,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=ft.border_radius.only(top_left=5, top_right=5),
        margin=ft.margin.only(bottom=0)
    )
