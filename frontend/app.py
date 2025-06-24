import flet as ft
from flet_addresses import addresses_view
from flet_contacts import contacts_view
from flet_meetings import meetings_view
from flet_meetingrooms import meetingrooms_view
from flet_meetingacceptances import meetingacceptances_view
from flet_projects import projects_view
from flet_tasks import tasks_view


def main(page: ft.Page):
    page.title = "My Ticket App"
    page.window.width = 1600
    page.window.height = 700
    page.update()

    content = ft.Container(
        expand=True,
        margin=100,
        padding=0,
    )
    page.add(content)

    views = [
        tasks_view,
        meetings_view,
        meetingrooms_view,
        meetingacceptances_view,
        contacts_view,
        addresses_view,
        projects_view,
    ]

    drawer_items = [
        ft.NavigationDrawerDestination(icon="task", label="Taken"),
        ft.NavigationDrawerDestination(icon="event", label="Vergaderingen"),
        ft.NavigationDrawerDestination(icon="meeting_room", label="Vergaderzalen"),
        ft.NavigationDrawerDestination(icon="check_circle", label="Deelnemerstatussen"),
        ft.NavigationDrawerDestination(icon="contact_page", label="Personen"),
        ft.NavigationDrawerDestination(icon="map", label="Adressen"),
        ft.NavigationDrawerDestination(icon="business", label="Projecten"),
    ]

    def show_view(view_func, title=None):
        content.content = view_func(page)
        if title:
            page.appbar.title.value = title
        page.update()

    def show_view_by_index(index):
        title = drawer_items[index].label
        show_view(views[index], title)
        page.drawer.open = False
        page.update()

    drawer = ft.NavigationDrawer(
        controls=drawer_items,
        on_change=lambda e: show_view_by_index(e.control.selected_index),
    )

    page.drawer = drawer
    page.appbar = ft.AppBar(
        title=ft.Text("Taken"),
        leading=ft.IconButton(icon="menu", on_click=lambda _: page.open(drawer)),
        bgcolor=ft.Colors.TRANSPARENT,
    )

    # Show initial view
    show_view(views[0])


ft.app(target=main)
