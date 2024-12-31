import threading
from AIStudio import main as main_ai
from HomeStudio import main
from SavedStudio import main as main_saved
from SavedStudio.main import *


class UI:

    def __init__(self, screen: Page):
        self.screen = screen
        self.duration = 1000
        self.__count__: int = 0
        self.animation_name = animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED
        self.screen.window.bgcolor = Colors.TRANSPARENT
        self.screen.padding = 0
        self.screen.spacing = 0
        self.screen.vertical_alignment = MainAxisAlignment.START
        self.screen.horizontal_alignment = CrossAxisAlignment.END
        self.screen.bgcolor = Colors.TRANSPARENT
        self.screen.window.always_on_top = True
        self.screen.window.top = 10
        self.screen.window.height = 40
        self.screen.window.width = 40
        self.screen.dark_theme = Theme(
            color_scheme=ColorScheme(primary="#2b2b2b", on_primary="#bdbdbd", on_secondary_container="#1c1c1c",
                                     tertiary_container=Colors.GREY_400, error="#2b2b2b", primary_container=Colors.GREY_800),
            font_family="roboto",
            use_material3=True, scrollbar_theme=ScrollbarTheme(thumb_visibility=False,
                                                               thumb_color=Colors.TRANSPARENT,
                                                               track_color=Colors.TRANSPARENT,
                                                               interactive=False,
                                                               track_visibility=False,
                                                               track_border_color=Colors.TRANSPARENT,
                                                               ))
        self.screen.theme = Theme(use_material3=True, font_family="roboto",
                                  color_scheme=ColorScheme(primary="#ffffff", on_primary=Colors.BLACK, error=Colors.GREY,
                                                           primary_container="#e3e3e3",
                                                           on_secondary_container="#d9d9d9", tertiary_container=Colors.GREY_800),
                                  scrollbar_theme=ScrollbarTheme(thumb_visibility=False,
                                                                 thumb_color=Colors.TRANSPARENT,
                                                                 track_color=Colors.TRANSPARENT,
                                                                 interactive=False,
                                                                 track_visibility=False,
                                                                 track_border_color=Colors.TRANSPARENT,
                                                                 )
                                  )
        self.screen.theme_mode = ThemeMode.LIGHT
        self.screen.overlay.append(main.Constants.notify_search_loading)
        self.screen.overlay.append(main_saved.Properties.notify_search_loading)
        self.screen.window.left = screen.width + 127
        self.screen.views.append(
            self.ui(),
        )
        self.screen.window.on_event = self.__window_event
        self.screen.update()
        threading.Thread(target=main_ai.AI().expand_window, kwargs={"app_ins": self}).start()

    def start_saved_main(self, e: WindowEvent):
        self.screen.window.height = 40
        self.screen.window.width = 40
        self.screen.window.top = 10
        self.screen.window.left = 1265 + 127
        self.screen.update()

        for _ in range(0, len(e.page.views) - 1):
            e.page.views.pop()

        e.page.views.append(
            self.ui(),
        )
        self.screen.go("/")
        self.screen.views[1].controls[0].on_click = self._expand_
        self.screen.views[1].controls[0].content = self.__original().content
        self.screen.views[1].controls[0].data = 2
        self.screen.views[1].update()

    def __window_event(self, e: WindowEvent):
        if e.data == "blur":
            self.count = 0
            if self.screen.route == "/":
                threading.Thread(target=main_ai.AI().expand_window, kwargs={"app_ins": self}).start()

            if self.screen.route == "/.":
                self.screen.views[-1].controls[0].width = 40
                self.screen.views[-1].controls[0].height = 40
                self.screen.views[-1].controls[0].on_click = self._expand_
                self.screen.views[-1].controls[0].content = self.__original().content
                self.screen.views[-1].controls[0].data = 2
                self.screen.views[-1].update()
                threading.Thread(target=main_ai.AI().expand_window, kwargs={"app_ins": self}).start()

            elif self.screen.route == "/saved":
                self.screen.views[-1].controls[0].height = 40
                self.screen.views[-1].controls[0].width = 40
                self.screen.views[-1].controls[0].update()
                threading.Thread(target=main_ai.AI().expand_window, kwargs={"app_ins": self}).start()
                threading.Timer(interval=1.2, function=self.start_saved_main, kwargs={"e": e}).start()

            elif self.count == 0:
                self.screen.views[-1].controls[0].width = 40
                self.screen.views[-1].controls[0].height = 40
                self.screen.views[-1].controls[0].on_click = self._expand_
                self.screen.views[-1].controls[0].content = self.__original().content
                self.screen.views[-1].controls[0].data = 2
                self.screen.views[-1].update()
                if self.__count__ == 2:
                    pass
                # threading.Thread(target=main_ai.AI().expand_window, kwargs={"app_ins": self}).start()
        cout(e.data)

    def __close_all(self, e: ControlEvent):
        if main.Variable.see_all_state:
            e.page.views[1].controls[0].content.content.content.controls[3].controls[0].content.controls[
                2].controls.extend(main.Home()._add_history(
                []
            ))
            main.Variable.see_all_state = False
            cout("see all closed")

    def _expand_(self, e: ControlEvent):
        # e.page.window.left = self.screen.window.left - 100
        self.screen.window.height = 800 or 650
        self.screen.window.width = 500
        self.screen.window.top = 10
        self.screen.window.left = 1275 - self.screen.window.width // 2
        self.screen.update()

        self.screen.views[-1].controls[0].width = 500
        self.screen.views[-1].controls[0].height = 800 or 650
        self.screen.views[-1].controls[0].border_radius = border_radius.all(15)

        if self.screen.route == "/":
            self.screen.views[-1].controls[0].on_click = lambda y: self.__close_all(y)
        elif self.screen.route == "/saved":
            pass
        elif self.screen.route == "/games":
            pass

        self.screen.views[-1].controls[0].data = 0
        self.screen.views[-1].controls[0].content = main.Home()._content_(e)
        main.Variable.counts = 0
        self.screen.update()

        main.ApiCont.daily_word_gen(screen=self.screen)

    def __size_anim(self, e: ControlEvent):
        if e.control.data == 2:
            self.screen.window.height = 40
            self.screen.window.width = 40
            self.screen.window.top = 10
            self.screen.window.left = 1265 + 127
            self.screen.update()

    def __original(self):
        return Container(
            on_click=self._expand_,
            animate_size=animation.Animation(self.duration, self.animation_name),
            on_animation_end=self.__size_anim,
            animate=animation.Animation(self.duration, self.animation_name),
            width=40, height=40, border_radius=border_radius.all(15),
            bgcolor=Colors.PRIMARY,
            content=Icon(
                name=Icons.SEARCH_ROUNDED,
                color=Colors.ON_PRIMARY,
                size=30,
            ),
        )

    def ui(self):
        _ = View(
            route="/",
            bgcolor=Colors.TRANSPARENT,
            padding=0, spacing=0,
            vertical_alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.END,
            controls=[
                self.__original(),
            ],
        )

        return _
