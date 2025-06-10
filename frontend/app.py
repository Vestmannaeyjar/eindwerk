import flet as ft
from flet_addresses import addresses_view
from flet_contacts import contacts_view
from flet_meetings import meetings_view
from flet_meetingrooms import meetingrooms_view
from flet_meetingacceptances import meetingacceptances_view
from flet_tasks import tasks_view


def main(page: ft.Page):
    page.title = "My Ticket App"

    content = ft.Container(expand=True)
    page.add(content)

    views = [
        meetings_view,
        meetingrooms_view,
        meetingacceptances_view,
        tasks_view,  # Tasks
        tasks_view,  # Actions
        tasks_view,  # Tags
        tasks_view,  # Tasktypes
        contacts_view,
        addresses_view,
        tasks_view,  # Projects
        tasks_view,  # Cycles
    ]

    drawer_items = [
        ft.NavigationDrawerDestination(icon="event", label="Meetings"),
        ft.NavigationDrawerDestination(icon="meeting_room", label="Meetingrooms"),
        ft.NavigationDrawerDestination(icon="check_circle", label="Meetingacceptances"),
        ft.NavigationDrawerDestination(icon="task", label="Tasks"),
        ft.NavigationDrawerDestination(icon="bolt", label="Actions"),
        ft.NavigationDrawerDestination(icon="label", label="Tags"),
        ft.NavigationDrawerDestination(icon="category", label="Tasktypes"),
        ft.NavigationDrawerDestination(icon="contact_page", label="Contacts"),
        ft.NavigationDrawerDestination(icon="map", label="Addresses"),
        ft.NavigationDrawerDestination(icon="business", label="Projects"),
        ft.NavigationDrawerDestination(icon="repeat", label="Cycles"),
    ]

    def show_view(view_func):
        content.content = view_func(page)
        page.update()

    def show_view_by_index(index):
        show_view(views[index])
        page.drawer.open = False
        page.update()

    drawer = ft.NavigationDrawer(
        controls=drawer_items,
        on_change=lambda e: show_view_by_index(e.control.selected_index),
    )

    page.drawer = drawer
    page.appbar = ft.AppBar(
        title=ft.Text("My Ticket App"),
        leading=ft.IconButton(icon="menu", on_click=lambda _: page.open(drawer)),
        bgcolor=ft.Colors.BLUE_300
    )

    # Show initial view
    show_view(views[0])


ft.app(target=main)
