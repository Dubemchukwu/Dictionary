import time
from flet import *
from MiniStudio import main
from nltk.corpus import words


# import flet

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

        screen.fonts = {"jetbrains_mono": "assets/ttf/JetBrainsMono-Regular.ttf"}
        screen.theme = Theme(font_family="jetbrains_mono")
        # screen.on_view_pop = view_pop
        screen.window.frameless = True
        main.UI(screen)
        screen.update()

        # while True:
        #     pass
            # print("he is also")



class Run:
    def __init__(self):
        app(Main)


if __name__ == "__main__":
    Run()
