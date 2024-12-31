from MiniStudio.main import *


class Main:
    def route_change(self, e: RouteChangeEvent):
        e.page.views.clear()
        e.page.views.append(
            ...
        )

    def __init__(self, screen: Page):

        def view_pop(e):
            screen.views.pop()
            top_view = screen.views[-1]
            screen.go(top_view.route)

        def route_change(event: RouteChangeEvent):
            cout(event.route)
            if event.route == "/saved":
                screen.views.append(
                    SavedPage().content(event),
                )
                screen.update()
            if event.route == "/.":
                for view in reversed(screen.views):
                    if view.route != "/":
                        screen.views.remove(view)

                cout(len(screen.views))

                screen.update()


        screen.fonts = {"lexend": "assets/Lexend/static/Lexend-Regular.ttf",
                        "lexend_light": "assets/Lexend/static/Lexend-Light.ttf",
                        "lexend_semi_bold": "assets/Lexend/static/Lexend-SemiBold.ttf",
                        "roboto": "assets/Roboto/static/Roboto-Regular.ttf",
                        "roboto_mono": "assets/Roboto_Mono/RobotoMono-VariableFont_wght.ttf",
                        "roboto_medium": "assets/Roboto/static/Roboto-Medium.ttf",
                        "roboto_light": "assets/Roboto/static/Roboto-Light.ttf",
                        "spartan_light": "assets/League_Spartan/static/LeagueSpartan-Light.ttf",
                        "spartan_semi_bold": "assets/League_Spartan/static/LeagueSpartan-SemiBold.ttf",
                        "spartan_medium": "assets/League_Spartan/static/LeagueSpartan-Medium.ttf",
                        "roboto_light_italic": "assets/Roboto/static/Roboto-LightItalic.ttf",
                        "spartan": "assets/League_Spartan/static/LeagueSpartan-Regular.ttf",
                        "inter_light": "assets/Inter/Inter-VariableFont_opsz_wght.ttf",
                        "krona_one": "assets/Krona_One/KronaOne-Regular.ttf"}
        screen.theme = Theme(font_family="roboto",
                             scrollbar_theme=ScrollbarTheme(thumb_visibility=False,
                                                            thumb_color=Colors.TRANSPARENT, track_color=Colors.TRANSPARENT,
                                                            interactive=False,
                                                            track_visibility=False,
                                                            track_border_color=Colors.TRANSPARENT,
                                                            ))
        # screen.on_view_pop = view_pop
        screen.window.frameless = True
        screen.on_route_change = route_change
        screen.go("/")
        mini_app_ = UI(screen)
        screen.update()



class Run:
    def __init__(self):
        app(Main)


if __name__ == "__main__":
    Run()
