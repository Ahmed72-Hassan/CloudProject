from flet import *
from Login import Login
from Signup import Signup
from first_interface import first
from Second_interface import Second
from Server_Functions import Server

def main(page: Page):
    page.padding = 0
    page.spacing = 0
    page.window.resizable = page.window.maximized = True
    page.scroll = ScrollMode.AUTO
    page.theme_mode = ThemeMode.LIGHT
    page.fonts = {"Alex": r"font/3.ttf", "Andalus": r"font/2.ttf", "Pac": r"font/Pacifico-Regular.ttf"}
    page.window.center()

    try:
        if Server.get_user_activiate_state(page) == 0:
            page.go("/")
        else:
            page.go("/first")
    except:
        page.go("/signup")

    def on_change_route(e):
        if page.route == "/" and Server.get_user_activiate_state(page) == 0:
            page.views.append(View("/", controls=[Login(page=page, on_signup=lambda e: page.go("/signup"),
                                                           on_success=lambda e: page.go("/first"))], padding=0))
        elif page.route == "/first" and Server.get_user_activiate_state(page) == 1:
            first_interface = first(page=page)
            page.views.append(View("/first", controls=[first_interface], padding=0, scroll=ScrollMode.AUTO,
                                   drawer=first_interface.drawer))

        elif page.route == "/signup":
            page.views.append(View("/signup", controls=[Signup(page=page, on_login=lambda e: page.go("/"),
                                                                on_success=lambda e: page.go("/first"))], padding=0))

        elif page.route == "/second":
            first_interface = first(page=page)
            second_interface = Second(page=page, first_interface=first_interface)
            page.views.append(View("/second", controls=[second_interface], padding=0, scroll=ScrollMode.AUTO,
                                   drawer=first_interface.drawer))
            first_interface.drawer.selected_index = 1

        page.update()


    def page_go(e):
        page.views.pop() 
        back_page = page.views[-1] 
        page.go(back_page.route)  
        page.update()

    page.on_route_change = on_change_route
    page.on_view_pop = page_go
    page.go(page.route)
    page.update()


app(target=main, assets_dir="assets", view=AppView.WEB_BROWSER, port=8080)
