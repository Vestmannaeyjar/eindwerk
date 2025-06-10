import flet as ft
import requests
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
import math


def paginated_list_view(
    page: ft.Page,
    title: str,
    api_base_url: str,
    render_item_row,
    build_edit_form,
    build_payload
):
    container = ft.Column()
    items_column = ft.Column()
    page.scroll = "auto"
    page.title = title

    current_item_id = None
    current_data = {}
    search_term = ""
    next_page_url = None
    prev_page_url = None
    current_page_url = api_base_url

    total_results_text = ft.Text()
    page_status_text = ft.Text()
    search_input = ft.TextField(label=f"Search {title.lower()}", width=300)

    def update_urls_with_search(url):
        if not url:
            return None
        parsed = urlparse(url)
        q = parse_qs(parsed.query)
        if search_term:
            q["search"] = [search_term]
        else:
            q.pop("search", None)
        q_flat = {k: v[0] for k, v in q.items()}
        return urlunparse(parsed._replace(query=urlencode(q_flat)))

    def load_items(url=None):
        nonlocal next_page_url, prev_page_url, current_page_url
        if not url:
            url = api_base_url
        current_page_url = update_urls_with_search(url)
        items_column.controls.clear()
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

            total_results_text.value = f"Total: {total_count}"
            page_status_text.value = f"Page {current_page_num} of {total_pages}"

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
                page.snack_bar = ft.SnackBar(ft.Text(f"{title} deleted"))
                delete_dialog.open = False
                load_items()
            except Exception as err:
                page.snack_bar = ft.SnackBar(ft.Text(f"Delete failed: {err}"))
            page.snack_bar.open = True
            page.update()

        delete_dialog.title = ft.Text("Confirm delete")
        delete_dialog.content = ft.Text("Are you sure?")
        delete_dialog.actions = [
            ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
            ft.ElevatedButton("Delete", on_click=confirm_delete),
        ]
        page.dialog = delete_dialog
        page.open(delete_dialog)
        page.update()

    def close_dialog():
        delete_dialog.open = False
        page.update()

    def open_edit_dialog(item=None):
        nonlocal current_item_id, current_data
        current_item_id = item["id"] if item else None
        current_data = item or {}
        edit_dialog.content = build_edit_form(current_data, submit_edit, cancel_edit)
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
            page.snack_bar = ft.SnackBar(ft.Text(f"{title} saved successfully"))
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

    prev_button = ft.ElevatedButton("Previous", on_click=lambda e: load_items(prev_page_url), disabled=True)
    next_button = ft.ElevatedButton("Next", on_click=lambda e: load_items(next_page_url), disabled=True)

    search_input.on_change = on_search
    add_button = ft.ElevatedButton(f"Add {title[:-1]}", on_click=lambda e: open_edit_dialog(None))

    edit_dialog = ft.AlertDialog(modal=True, title=ft.Text(f"Edit {title[:-1]}"), actions_alignment=ft.MainAxisAlignment.END)
    delete_dialog = ft.AlertDialog(modal=True, actions_alignment=ft.MainAxisAlignment.END)

    container.controls.extend([
        search_input,
        total_results_text,
        items_column,
        page_status_text,
        ft.Row([prev_button, next_button], alignment=ft.MainAxisAlignment.CENTER),
        add_button,
    ])

    load_items()
    return container
