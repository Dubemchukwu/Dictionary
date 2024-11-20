from flet import *
import icecream
from HomeStudio import main

cout = icecream.ic


class UI:

    def __init__(self, screen):
        self.screen = screen
        self.duration = 1000
        self.animation_name = animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED
        self.screen.window.bgcolor = colors.TRANSPARENT
        self.screen.padding = 0
        self.screen.spacing = 0
        self.screen.vertical_alignment = MainAxisAlignment.START
        self.screen.horizontal_alignment = CrossAxisAlignment.END
        self.screen.bgcolor = colors.TRANSPARENT
        self.screen.window.always_on_top = True
        self.screen.window.top = 10
        self.screen.window.height = 40
        self.screen.window.width = 40
        self.screen.window.left = screen.width + 127
        self.screen.views.append(
            self.__ui(),
        )
        self.screen.window.on_event = self.__window_event
        self.screen.update()

    def __window_event(self, e: WindowEvent):
        if e.data == "blur":
            self.count = 0
            if self.count == 0:
                self.screen.views[1].controls[0].width = 40
                self.screen.views[1].controls[0].height = 40
                self.screen.views[1].controls[0].on_click = self.__expand_
                self.screen.views[1].controls[0].content = self.__original().content
                self.screen.views[1].controls[0].data = 2
                self.screen.views[1].update()

        cout(e.data)

    def __close_all(self, e: ControlEvent):
        if main.Variable.see_all_state:
            e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[2].controls.extend(main.Home()._add_history(
                []
            ))
            main.Variable.see_all_state = False
            cout("see all closed")

    def __expand_(self, e: ControlEvent):
        # e.page.window.left = self.screen.window.left - 100
        self.screen.window.height = 800 or 650
        self.screen.window.width = 500
        self.screen.window.top = 10
        self.screen.window.left = 1275 - self.screen.window.width // 2
        self.screen.update()
        e.control.width = 500
        e.control.height = 800 or 650
        e.control.border_radius = border_radius.all(15)
        e.control.on_click = lambda y: self.__close_all(y)
        e.control.data = 0
        e.page.views[1].controls[0].content = main.Home()._content_()
        main.Variable.counts = 0
        e.control.update()

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
            on_click=self.__expand_,
            animate_size=animation.Animation(self.duration, self.animation_name),
            on_animation_end=self.__size_anim,
            animate=animation.Animation(self.duration, self.animation_name),
            width=40, height=40, border_radius=border_radius.all(15),
            bgcolor="#ffffff", content=Icon(
                name=icons.SEARCH_ROUNDED,
                color=colors.BLACK,
                size=30,
            ),
        )

    def __ui(self):
        _ = View(
            route="/",
            bgcolor=colors.TRANSPARENT,
            padding=0, spacing=0,
            vertical_alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.END,
            controls=[
                self.__original(),
            ],
        )

        return _
