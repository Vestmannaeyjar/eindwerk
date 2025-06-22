import flet as ft
import requests
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
import math


def paginated_list_view(
    page: ft.Page,
    title: str,
    item_description: str,
    api_base_url: str,
    render_item_row,
    build_edit_form,
    build_payload,
    render_header=None
):
    container = ft.Column()
    items_column = ft.Column()
    page.scroll = "auto"
    page.title = f"My ticket app / {title}"

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
            ft.TextButton("Annuleer", on_click=lambda e: close_dialog()),
            ft.ElevatedButton("Verwijder", on_click=confirm_delete),
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

    prev_button = ft.ElevatedButton("Vorige", on_click=lambda e: load_items(prev_page_url), disabled=True)
    next_button = ft.ElevatedButton("Volgende", on_click=lambda e: load_items(next_page_url), disabled=True)

    search_input.on_change = on_search
    add_button = ft.ElevatedButton(f"Voeg een {item_description} toe", on_click=lambda e: open_edit_dialog(None))

    edit_dialog = ft.AlertDialog(modal=True, title=ft.Text(f"Bewerk {item_description}"), actions_alignment=ft.MainAxisAlignment.END)
    delete_dialog = ft.AlertDialog(modal=True, actions_alignment=ft.MainAxisAlignment.END)

    top_controls = ft.Row(
        [
            add_button,
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
