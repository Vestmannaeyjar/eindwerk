import flet as ft


def render_row(data, fields, edit_cb, delete_cb):
    return ft.Row([
        ft.IconButton(icon="edit", tooltip="Edit", on_click=lambda e: edit_cb(data)),
        ft.IconButton(icon="delete", tooltip="Delete", on_click=lambda e: delete_cb(data["id"])),
        *[
            ft.Container(content=ft.Text(str(data.get(f["key"], ""))), width=f["width"])
            for f in fields
        ]
    ])
