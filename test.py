import random
import threading

from english_words import get_english_words_set
from flet import *
import requests

real_words = []


def add_file(word__: str):
    with open("DataStudio/dic_words.txt", "a") as file:
        file.write(word__ + "\n")


def get_words():
    words = list(get_english_words_set(["web2"], alpha=True, lower=True))
    for word_ in words:
        def doit():
            response = requests.get(
                f"https://dictionaryapi.com/api/v3/references/sd4/json/{word_}?key=166e17cb-08dd-4439-a142"
                f"-85763906e46d",
            )
            try:
                if type(response.json()[0]) == dict:
                    real_words.append(word_)
                    add_file(word_)
                    print(response.json()[0]["fl"], word_)
            except TypeError as e:
                pass
            except ConnectionError as e:
                doit()
                print(e)
            except IndexError as e:
                pass
            except KeyError as e:
                pass

        doit()


def edit_file():
    new_data = []
    with open("DataStudio/words.txt", "r") as file:
        data = file.read()
        data = data.split("\n")
        for i in data:
            if len(i) > 2:
                new_data.append(i)
    return new_data


def create_file():
    get_words()
    _words_ = real_words
    _words_.sort()
    words_ = ""
    for word in _words_:
        words_ += word + "\n"
    with open("DataStudio/words.txt", "w") as file:
        file.write(words_)
    print(words_)


class Widget:
    def __init__(self, amount: int, screen):
        self.amt = amount
        self.colors = dir(colors)
        self.colors.remove("with_opacity")
        threading.Timer(interval=1, function=self.build, kwargs={"event": screen}).start()

    def build(self, event):
        for i in range(self.amt):
            event.views[-1].controls[0].content.content.controls.insert(
                1,
                Container(
                    bgcolor=str(random.choice(self.colors)).lower().replace("_",""),
                    height=40, alignment=alignment.center,
                    content=Text("RAM"),
                ),
            )
            event.views[-1].controls[0].content.content.update()



def Screen(screen: Page):
    screen.window.center()

    hf = HapticFeedback()

    def change_page(e: ControlEvent):
        hf.vibrate()
        hf.heavy_impact()
        hf.light_impact()
        hf.medium_impact()
        hf.update()
        e.page.go(e.control.data)

    def add_back_button(e: HoverEvent):
        if e.local_x <= 100.0:
            e.control.content.controls[-1].offset = (0, 0)
            e.control.content.controls[-1].update()
        elif e.local_x >= 1140.0:
            if e.control.content.controls[-2].data == "about":
                e.control.content.controls[-2].offset = (-0.5, 0)
                e.control.content.controls[-2].update()
        else:
            e.control.content.controls[-1].offset = (-1, 0)
            e.control.content.controls[-1].update()
            if e.control.content.controls[-2].data == "about":
                e.control.content.controls[-2].offset = (2, 0)
                e.control.content.controls[-2].update()

    def back(e: ControlEvent):
        e.page.views[-1].controls[0].content.controls[-1].offset = (-1, 0)
        e.page.views[-1].controls[0].content.controls[-1].update()

        if e.control.data == "about":
            e.page.views[-1].controls[0].content.controls[-2].offset = (2, 0)
            e.page.views[-1].controls[0].content.controls[-2].update()

        routes.pop()
        e.page.go(routes[-1])
        print(e.data, "Tapped")

    def back_tap(e: ControlEvent):
        routes.pop()
        e.page.go(routes[-1])
        print(e.data, "Tapped")

    def goto_others(e: ControlEvent):
        e.page.go("/other")
        Widget(90, screen)

    home_ = View(
        route="/",
        controls=[
            Container(
                expand=True,
                bgcolor=colors.RED, alignment=alignment.center,
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("HOme", size=30, color=colors.BLACK),
                        ElevatedButton(text="About", data="/about", on_click=lambda e: change_page(e),
                                       bgcolor=colors.TRANSPARENT, color=colors.BLACK),
                        ElevatedButton(text="Settings", data="/set", on_click=lambda e: change_page(e),
                                       bgcolor=colors.TRANSPARENT, color=colors.BLACK),
                        ElevatedButton(text="Others", data="/other", on_click=lambda e: goto_others(e),
                                       bgcolor=colors.TRANSPARENT, color=colors.BLACK),
                    ],
                ),
            ),
        ],
    )

    about_ = View(
        route="/about",
        controls=[
            GestureDetector(
                expand=True,
                on_scroll=lambda e: print("hi, everyone"),
                content=Stack(
                    alignment=alignment.center_left,
                    controls=[
                        Container(
                            bgcolor=colors.BLUE, alignment=alignment.center,
                            content=Text("AboUt", size=35, color=colors.BLACK),
                        ),

                        TransparentPointer(
                            data="about",
                            offset=(2, 0),
                            expand=True,
                            right=-0.5,
                            animate_offset=Animation(1750, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                            content=IconButton(
                                icon_size=40,
                                data="about",
                                on_click=back,
                                width=54, height=54,
                                icon=icons.CHEVRON_RIGHT,
                                style=ButtonStyle(
                                    shape=CircleBorder(),
                                    surface_tint_color=colors.BLACK45,
                                    bgcolor=colors.with_opacity(0.7, colors.WHITE),
                                    icon_color=colors.BLUE,
                                ),
                            ),
                        ),

                        TransparentPointer(
                            offset=(-1, 0),
                            expand=False,
                            expand_loose=False,
                            animate_offset=Animation(1750, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                            height=800, width=100,
                            content=IconButton(
                                icon_size=70,
                                data="about",
                                on_click=back,
                                width=40, height=40,
                                scale=0.55,
                                icon=icons.CHEVRON_LEFT,
                                style=ButtonStyle(
                                    shape=CircleBorder(),
                                    surface_tint_color=colors.BLACK45,
                                    bgcolor=colors.with_opacity(0.7, colors.WHITE),
                                    icon_color=colors.BLUE,
                                ),
                            ),
                        ),
                    ],
                ),
                on_hover=add_back_button,
            ),
        ],
    )

    settings = View(
        route="/set",
        controls=[
            GestureDetector(
                expand=True,
                content=Stack(
                    alignment=alignment.center_left,
                    controls=[Container(
                        bgcolor=colors.GREEN, alignment=alignment.center,
                        content=Text("Settings", size=35, color=colors.BLACK),
                    ),
                        TransparentPointer(
                            offset=(-1, 0),
                            expand=False,
                            expand_loose=False,
                            animate_offset=Animation(1750, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                            height=800, width=100,
                            content=IconButton(
                                icon_size=70,
                                on_click=back,
                                width=40, height=40,
                                scale=0.55,
                                icon=icons.CHEVRON_LEFT,
                                style=ButtonStyle(
                                    shape=CircleBorder(),
                                    surface_tint_color=colors.BLACK45,
                                    bgcolor=colors.with_opacity(0.7, colors.WHITE),
                                    icon_color=colors.GREEN,
                                ),
                            ),
                        ),
                    ],
                ),
                on_hover=add_back_button,
            ),
        ],
    )

    others = View(
        route="/other",
        controls=[
            GestureDetector(
                expand=True,
                on_secondary_tap=lambda e: back_tap(e),
                content=Container(
                    bgcolor=colors.ORANGE, alignment=alignment.center,
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        scroll=ScrollMode.AUTO,
                        controls=[
                            Text("OthErs", size=35, color=colors.BLACK),
                            TransparentPointer(height=50),
                        ],
                    ),
                ),
            ),
        ],
    )

    views_handler = {
        '/': home_,
        '/about': about_,
        '/set': settings,
        '/other': others,
    }

    routes = []

    def route_change(route):
        print(screen.route)
        routes.append(screen.route)
        screen.views.clear()
        screen.views.append(
            views_handler[screen.route],
        )
        screen.update()

    screen.overlay.append(hf)
    screen.on_route_change = route_change
    screen.go("/")
    screen.update()



import flet as ft

def main(page: ft.Page):
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    pb = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Item 1"),
            ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, text="Check power"),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),
                        ft.Text("Item with a custom content"),
                    ]
                ),
                on_click=lambda _: print("Button with a custom content clicked!"),
            ),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(
                text="Checked item", checked=False, on_click=check_item_clicked
            ),
        ]
    )
    page.add(pb)

ft.app(main)


# app(target=Screen)
# get_words()
