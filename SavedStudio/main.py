from flet import *
import math
from SavedStudio.utilities import *
from HomeStudio.main import Variable
from PIL import ImageFont


class Properties:
    def __init__(self):
        self.name: str = "saved"



class PrimaryFunction:

    def animate_refresh(self, e: ControlEvent):
        e.control.rotate = e.control.rotate + math.pi * 2
        e.control.update()

    def refresh_all(self, e: ControlEvent):
        temp_screen = e.page.views[-1]
        e.page.views.pop()
        e.page.views.append(
            temp_screen,
        )
        e.page.update()


class SWidget(Row):

    def __init__(self, text: str):
        super().__init__()
        self.controls = [_Widget(text)]


class _Widget(Container):

    def cal_width(self) -> float:
        font = ImageFont.truetype("assets/Lexend/static/Lexend-Regular.ttf", 18)
        width = font.getlength(self.text)
        # width = (len(self.text) * 16) + 55
        return width + len(self.text)

    def __init__(self, text: str):
        super().__init__()
        self.text = text
        self.width = self.cal_width() + 70
        self.bgcolor = "#afafaf"
        self.expand_loose = False
        self.border_radius = border_radius.all(13)
        self.on_click = lambda e: cout(e.name)
        self.alignment = alignment.center_left
        self.height = 45
        self.padding = padding.only(left=10)
        self.content = self.content__()

    def remove_saved(self, e: ControlEvent):
        e.control.offset = (1, 0)
        e.control.rotate = math.pi
        e.control.selected = not e.control.selected
        e.control.update()

    def end_animate_remove(self, e: ControlEvent):
        e.control.rotate = 0
        e.control.offset = (0, 0)
        e.control.update()

    def content__(self):
        return Row(
            expand=False,
            expand_loose=False,
            width=self.width - 15,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            run_spacing=0, spacing=0,
            controls=[
                Container(
                    width=self.cal_width() + 8,
                    content=Text(
                        value=self.text,
                        overflow=TextOverflow.ELLIPSIS if len(self.text) * 16 > 200 else TextOverflow.VISIBLE,
                        style=TextStyle(
                            font_family="lexend",
                            size=18, weight=FontWeight.W_400,
                            color=Colors.BLACK,
                            letter_spacing=1,
                        ),
                    ),
                ),
                IconButton(
                    icon=Icons.BOOKMARK_ROUNDED, rotate=0, offset=(0, 0),
                    on_animation_end=lambda e: self.end_animate_remove(e),
                    animate_offset=Animation(1000, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                    animate_rotation=Animation(1000, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                    selected_icon=Icons.BOOKMARK_OUTLINE_ROUNDED,
                    selected_icon_color=Colors.GREY_800,
                    icon_size=30, icon_color=Colors.GREY_800,
                    on_click=lambda e: self.remove_saved(e),
                    selected=False,
                    style=ButtonStyle(
                        overlay_color=Colors.TRANSPARENT,
                    ),
                ),
            ]
        )


class SavedPage:
    def __init__(self):
        self.test_list = [
            "Urdictionary V2", "apple", "banana", "cherry", "dog", "elephant", "flower", "guitar",
            "honey", "island", "jacket", "kangaroo", "lemon", "mountain", "notebook",
            "ocean", "pencil", "quartz", "rainbow", "sunshine", "tiger"
        ]

    def __add_back_button(self, e: HoverEvent):
        if e.control.data == Properties().name:
            if e.global_x <= e.page.width / 5:
                if e.global_x <= 30.0:
                    e.control.content.controls[-1].offset = (-1.75, 0)
                    e.control.content.controls[-1].update()
                else:
                    e.control.content.controls[-1].offset = (0.07, 0)
                    e.control.content.controls[-1].update()

            elif e.global_x >= e.page.width - (e.page.width / 5):
                if e.global_x >= 478.0:
                    e.control.content.controls[-2].offset = (1, 0)
                    e.control.content.controls[-2].update()
                else:
                    e.control.content.controls[-2].offset = (-0.75, 0)
                    e.control.content.controls[-2].update()
            else:
                e.control.content.controls[-1].offset = (-1.75, 0)
                e.control.content.controls[-1].update()
                e.control.content.controls[-2].offset = (1, 0)
                e.control.content.controls[-2].update()

    def __back(self, e: ControlEvent):
        if e.control.data == "left":
            e.control.offset = (-1.75, 0)
            e.control.update()
        else:
            e.control.offset = (1, 0)
            e.control.update()

        e.page.go("/")
        e.page.views.pop()
        e.page.update()

    def change_screen(self, e: ControlEvent):
        if e.control.data == "saved":
            e.page.go("/saved")
            cout(e.page.route)
        elif e.control.data == "games":
            pass

    def __main_content(self, e):
        return Container(
            animate_size=Animation(1000, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
            animate=Animation(1000, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
            width=e.page.window.width,
            height=e.page.window.height,
            bgcolor="#ffffff",
            border_radius=border_radius.all(15),
            shadow=BoxShadow(spread_radius=8, blur_radius=1,
                             blur_style=ShadowBlurStyle.OUTER,
                             color=Colors.with_opacity(0.75,
                                                       Colors.BLACK),
                             offset=(0, .0023),
                             ),
            padding=padding.symmetric(0, 20),
            content=GestureDetector(
                data=Properties().name,
                expand=True,
                on_hover=self.__add_back_button,
                content=Stack(
                    alignment=alignment.top_center,
                    controls=[
                        Column(
                            alignment=MainAxisAlignment.END,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Text(
                                            size=30,
                                            spans=[
                                                TextSpan("D",
                                                         style=TextStyle(color="#9d0208"),
                                                         ),

                                                TextSpan("icti",
                                                         style=TextStyle(color=Colors.BLACK),
                                                         ),
                                                TextSpan("o",
                                                         style=TextStyle(color="#9d0208"),
                                                         ),
                                                TextSpan("nary",
                                                         style=TextStyle(color=Colors.BLACK),
                                                         ),
                                            ],
                                            font_family="krona_one",
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            vertical_alignment=CrossAxisAlignment.CENTER,
                                            controls=[
                                                IconButton(
                                                    icon=Icons.REFRESH_ROUNDED,
                                                    rotate=0,
                                                    style=ButtonStyle(
                                                        bgcolor=Colors.TRANSPARENT,
                                                        overlay_color={ControlState.DEFAULT: Colors.BLACK12,
                                                                       ControlState.PRESSED: Colors.BLACK12,
                                                                       ControlState.HOVERED: Colors.TRANSPARENT,
                                                                       },
                                                    ),
                                                    animate_rotation=animation.Animation(
                                                        1500,
                                                        AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                                    on_click=lambda e: PrimaryFunction().animate_refresh(e),
                                                    on_animation_end=lambda e: PrimaryFunction().refresh_all(e),
                                                    icon_size=30,
                                                    icon_color=Colors.BLACK,
                                                ),
                                                PopupMenuButton(
                                                    tooltip="",
                                                    bgcolor="#e3e3e3",
                                                    size_constraints=BoxConstraints(min_width=110, max_width=110),
                                                    rotate=0,
                                                    animate_rotation=Animation(1000,
                                                                               AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                                    on_open=Variable().refresh_all,
                                                    on_cancel=Variable().undo_refresh,
                                                    on_select=Variable().undo_refresh,
                                                    elevation=None,
                                                    menu_position=PopupMenuPosition.UNDER,
                                                    menu_padding=padding.only(top=15),
                                                    popup_animation_style=animation.AnimationStyle(500, 500,
                                                                                                   AnimationCurve.LINEAR_TO_EASE_OUT,
                                                                                                   AnimationCurve.LINEAR_TO_EASE_OUT),
                                                    shadow_color=Colors.TRANSPARENT,
                                                    surface_tint_color=Colors.TRANSPARENT,
                                                    icon=Icons.MORE_HORIZ_ROUNDED,
                                                    icon_size=30,
                                                    icon_color=Colors.BLACK,
                                                    items=[
                                                        PopupMenuItem(
                                                            content=Row(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    SegmentedButton(
                                                                        width=90,
                                                                        height=40,
                                                                        style=ButtonStyle(
                                                                            bgcolor={ControlState.SELECTED: "#999999",
                                                                                     ControlState.DEFAULT: "#d9d9d9"},
                                                                        ),
                                                                        show_selected_icon=False,
                                                                        selected={"light"},
                                                                        allow_empty_selection=False,
                                                                        allow_multiple_selection=False,
                                                                        on_change=lambda e: cout(
                                                                            list(e.control.selected)[0]),
                                                                        segments=[
                                                                            Segment(
                                                                                value="light",
                                                                                icon=Icon(
                                                                                    name=Icons.SUNNY,
                                                                                    size=20, color=Colors.BLACK,
                                                                                ),
                                                                            ),
                                                                            Segment(
                                                                                value="dark",
                                                                                icon=Icon(
                                                                                    name=Icons.SHIELD_MOON_ROUNDED,
                                                                                    size=20, color=Colors.BLACK,
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ),
                                                        PopupMenuItem(
                                                            on_click=self.change_screen,
                                                            data="saved",
                                                            content=Row(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    Text(
                                                                        text_align=TextAlign.CENTER,
                                                                        value="SAVED",
                                                                        font_family="spartan",
                                                                        weight=FontWeight.W_800,
                                                                        size=20,
                                                                        color="#1d3557",
                                                                    ),
                                                                ],
                                                            ),
                                                        ),
                                                        PopupMenuItem(
                                                            on_click=self.change_screen,
                                                            data="games",
                                                            content=Row(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    Text(
                                                                        text_align=TextAlign.CENTER,
                                                                        value="GAMES",
                                                                        color="#9d0208",
                                                                        font_family="spartan",
                                                                        weight=FontWeight.W_800,
                                                                        size=20,
                                                                    ),
                                                                ],
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                            ]
                                        )
                                    ],
                                ),
                                TransparentPointer(height=35),
                                Row(
                                    alignment=MainAxisAlignment.START,
                                    controls=[
                                        Text(
                                            value="SAVED",
                                            weight=FontWeight.W_500,
                                            color=Colors.BLACK,
                                            size=23,
                                            style=TextStyle(
                                                font_family="spartan_semi_bold",
                                                letter_spacing=3,
                                            ),
                                        ),
                                    ],
                                ),
                                Column(
                                    height=550,
                                    alignment=MainAxisAlignment.START,
                                    scroll=ScrollMode.ALWAYS,
                                    spacing=15, run_spacing=15,
                                    horizontal_alignment=CrossAxisAlignment.START,
                                    controls=[
                                        SWidget(text) for text in self.test_list
                                    ],
                                ),
                                TransparentPointer(height=10),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                    height=25,
                                    controls=[
                                        Text(
                                            spans=[
                                                TextSpan(
                                                    text="©",
                                                    style=TextStyle(
                                                        weight=FontWeight.W_500, color=Colors.BLACK,
                                                        size=17,
                                                        shadow=BoxShadow(spread_radius=8, blur_radius=1,
                                                                         blur_style=ShadowBlurStyle.OUTER,
                                                                         color=Colors.with_opacity(0.75,
                                                                                                   Colors.BLACK),
                                                                         offset=(0, .0023),
                                                                         ),
                                                    ),
                                                ),
                                                TextSpan(
                                                    text="NH-CEN Group4 PROJECT",
                                                    style=TextStyle(
                                                        weight=FontWeight.W_500, color=Colors.BLACK,
                                                        size=12,
                                                        shadow=BoxShadow(spread_radius=0, blur_radius=0,
                                                                         blur_style=ShadowBlurStyle.OUTER,
                                                                         color=Colors.with_opacity(0.75,
                                                                                                   Colors.BLACK),
                                                                         offset=(0, .0023),
                                                                         ),
                                                    ),
                                                )
                                            ],
                                            font_family="inter_light",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        IconButton(
                            offset=(1, 0),
                            data="right",
                            left=500 - 64,
                            top=e.page.window.height - e.page.window.height // 2 - 54 / 2,
                            animate_offset=Animation(1750, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                            icon_size=50,
                            expand=False,
                            on_click=self.__back,
                            width=64, height=64,
                            icon=Icons.CHEVRON_RIGHT_ROUNDED,
                            style=ButtonStyle(
                                shape=CircleBorder(),
                                overlay_color=Colors.TRANSPARENT,
                                surface_tint_color=Colors.BLACK45,
                                bgcolor=Colors.with_opacity(0.0, Colors.WHITE),
                                icon_color={ControlState.DEFAULT: "#26282e", ControlState.PRESSED: Colors.BLACK87},
                            ),
                        ),

                        IconButton(
                            offset=(-1.75, 0),
                            left=0,
                            data="left",
                            top=e.page.window.height - e.page.window.height // 2 - 54 / 2,
                            animate_offset=Animation(1750, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                            icon_size=50,
                            expand=False,
                            on_click=self.__back,
                            width=64, height=64,
                            icon=Icons.CHEVRON_LEFT_ROUNDED,
                            style=ButtonStyle(
                                shape=CircleBorder(),
                                overlay_color=Colors.TRANSPARENT,
                                surface_tint_color=Colors.BLACK45,
                                bgcolor=Colors.with_opacity(0.0, Colors.WHITE),
                                icon_color={ControlState.DEFAULT: "#26282e", ControlState.PRESSED: Colors.BLACK87},
                            ),
                        ),

                    ],
                ),
            ),
        )

    def content(self, _page):
        return View(
            route="/saved",
            bgcolor=Colors.TRANSPARENT,
            padding=0, spacing=0,
            vertical_alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.END,
            controls=[
                self.__main_content(_page),
            ],
        )
