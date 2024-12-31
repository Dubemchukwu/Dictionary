import threading

from flet import *
import math
from SavedStudio.utilities import *
from HomeStudio.main import Variable, Constants, SearchWidget, MeaningWidget
from PIL import ImageFont


class Properties:
    notification_text = Ref[Text]()
    notify_search_loading = SnackBar(
        on_visible=lambda e: Constants.open_up_snack(e),
        bgcolor=Colors.TRANSPARENT,
        elevation=0, duration=3000,
        behavior=SnackBarBehavior.FIXED,
        dismiss_direction=DismissDirection.START_TO_END,
        content=Row(
            height=60,
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Container(
                    width=70, height=30,
                    scale=0, on_animation_end=lambda e: Constants.end_animation(e),
                    animate_scale=Animation(1500, AnimationCurve.ELASTIC_OUT),
                    animate=Animation(1000, AnimationCurve.ELASTIC_IN),
                    shadow=[BoxShadow(
                        spread_radius=1,
                        color=Colors.with_opacity(0.45, Colors.ERROR),
                        offset=(0, 1),
                        blur_radius=1,
                    ),
                        BoxShadow(
                            spread_radius=1,
                            color=Colors.with_opacity(0.45, Colors.ERROR),
                            offset=(0, 1),
                            blur_radius=1,
                        )
                    ],
                    border_radius=6,
                    alignment=alignment.center,
                    bgcolor=Colors.ON_SECONDARY_CONTAINER,
                    content=Text(f"Deleting", size=13, text_align=TextAlign.CENTER, weight=FontWeight.W_600,
                                 ref=notification_text, color=Colors.ON_PRIMARY),
                ),
            ],
        ),
    )

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

    def __init__(self, _dic_: dict):
        super().__init__()
        self.controls = [_Widget(_dic_)]


class _Widget(Container):

    def cal_width(self) -> float:
        font = ImageFont.truetype("assets/Lexend/static/Lexend-Regular.ttf", 18)
        width = font.getlength(self.text)
        # width = (len(self.text) * 16) + 55
        return width + len(self.text)

    def __init__(self, dic_mn: dict):
        super().__init__()
        self.text = dic_mn["word"]
        self.width = self.cal_width() + 70
        self.bgcolor = Colors.ON_SECONDARY_CONTAINER
        self.expand_loose = False
        self.__count__: int = 0
        self.data = dic_mn
        self.border_radius = border_radius.all(13)
        self.on_click = self.open_saved_bookmark
        self.alignment = alignment.center_left
        self.height = 45
        self.padding = padding.only(left=10)
        self.content = self.content__()

    def open_saved_bookmark(self, e: ControlEvent):
        self.__count__ = 0
        e.data = e.control.data["word"]
        Variable.searched_word = e.data
        e.page.go("/.")
        Constants.animated_switcher.current.data = None
        SearchWidget._state_ = False
        Constants.animated_switcher.current.content = SearchWidget(e)
        search_widget = Constants.animated_switcher.current.content
        search_widget.controls[0].content.controls[1].controls[0].spans[1].text = e.control.data["pos"]
        search_widget.controls[0].content.controls[1].controls[1].visible = False
        e.page.views[-1].controls[0].content.content.content.controls[0].controls[2].controls[0].controls[1].value = e.data
        e.page.views[-1].controls[0].content.content.content.controls[0].controls[2].controls[0].controls[1].update()
        e.page.views[-1].controls[0].content.content.content.controls[0].controls[2].controls[1].visible = True
        e.page.views[-1].controls[0].content.content.content.controls[0].controls[2].controls[1].selected = Constants().get_search_saved_state(e.data)
        e.page.views[-1].controls[0].content.content.content.controls[0].controls[2].controls[1].update()
        if "searches" in e.control.data.keys():
            for data in e.control.data["searches"]:
                search_widget.controls[0].content.controls[1].controls.append(
                    MeaningWidget(
                        m_text=data["meaning"],
                        synonyms=data["synonyms"] or "Nothing to See Here",
                        antonyms=data["antonyms"] or "Nothing to See Here",
                    ).build(),
                )
        else:
            search_widget.controls[0].content.controls[1].controls.append(
                MeaningWidget(
                    m_text=e.control.data["meaning"],
                    synonyms="Nothing to See Here",
                    antonyms="Nothing to See Here",
                ).build(),
            )

        # search_widget.controls[0].content.update()
        Constants.animated_switcher.current.update()
        e.page.update()

    def remove_saved(self, e: ControlEvent):
        e.control.offset = (1, 0)
        e.control.rotate = math.pi
        e.control.selected = not e.control.selected
        e.control.update()
        Properties.notification_text.current.value = f"Deleting!"
        Properties.notify_search_loading.open = True
        Properties.notify_search_loading.update()
        if e.control.selected:
            threading.Thread(target=SaveUtils().remove_saved_items, kwargs={"word": e.control.data}).start()

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
                            color=Colors.ON_PRIMARY,
                            letter_spacing=1,
                        ),
                    ),
                ),
                IconButton(
                    data=self.text,
                    icon=Icons.BOOKMARK_ROUNDED, rotate=0, offset=(0, 0),
                    on_animation_end=lambda e: self.end_animate_remove(e),
                    animate_offset=Animation(1000, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                    animate_rotation=Animation(1000, AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                    selected_icon=Icons.BOOKMARK_OUTLINE_ROUNDED,
                    selected_icon_color=Colors.TERTIARY_CONTAINER,
                    icon_size=30, icon_color=Colors.TERTIARY_CONTAINER,
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
        _SaveUtils = SaveUtils()
        self.test_list = [
            "Urdictionary V2", "apple", "banana", "cherry", "dog", "elephant", "flower", "guitar",
            "honey", "island", "jacket", "kangaroo", "lemon", "mountain", "notebook",
            "ocean", "pencil", "quartz", "rainbow", "sunshine", "tiger"
        ]
        self.saved_items_list = _SaveUtils.get_saved_items()

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
            bgcolor=Colors.PRIMARY,
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
                                                         style=TextStyle(color=Colors.ON_PRIMARY),
                                                         ),
                                                TextSpan("o",
                                                         style=TextStyle(color="#9d0208"),
                                                         ),
                                                TextSpan("nary",
                                                         style=TextStyle(color=Colors.ON_PRIMARY),
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
                                                    icon_color=Colors.ON_PRIMARY,
                                                ),
                                                PopupMenuButton(
                                                    tooltip="",
                                                    bgcolor=Colors.PRIMARY_CONTAINER,
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
                                                    icon_color=Colors.ON_PRIMARY,
                                                    items=[
                                                        PopupMenuItem(
                                                            content=Row(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    SegmentedButton(
                                                                        width=90,
                                                                        height=40,
                                                                        style=ButtonStyle(
                                                                            color=Colors.TRANSPARENT,
                                                                            bgcolor=Colors.TRANSPARENT,
                                                                            overlay_color=Colors.TRANSPARENT,
                                                                        ),
                                                                        show_selected_icon=False,
                                                                        selected={e.page.theme_mode.value},
                                                                        allow_empty_selection=False,
                                                                        allow_multiple_selection=False,
                                                                        data="markdown",
                                                                        on_change=lambda e: Constants.change_theme(e),
                                                                        segments=[
                                                                            Segment(
                                                                                value="light",
                                                                                icon=Icon(
                                                                                    name=Icons.WB_SUNNY_ROUNDED if e.page.theme_mode.value == "light" else Icons.WB_SUNNY_OUTLINED,
                                                                                    size=20, color=Colors.ON_PRIMARY,
                                                                                ),
                                                                            ),
                                                                            Segment(
                                                                                value="dark",
                                                                                icon=Icon(
                                                                                    name=Icons.DARK_MODE_ROUNDED if e.page.theme_mode.value == "dark" else Icons.DARK_MODE_OUTLINED,
                                                                                    size=20, color=Colors.ON_PRIMARY,
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
                                                                        color=Colors.ON_PRIMARY,
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
                                            color=Colors.ON_PRIMARY,
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
                                        SWidget(text) for text in self.saved_items_list
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
                                                        weight=FontWeight.W_500, color=Colors.ON_PRIMARY,
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
                                                        weight=FontWeight.W_500, color=Colors.ON_PRIMARY,
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
                                icon_color={ControlState.DEFAULT: Colors.ON_PRIMARY, ControlState.PRESSED: Colors.BLACK87},
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
                                icon_color={ControlState.DEFAULT: Colors.ON_PRIMARY, ControlState.PRESSED: Colors.BLACK87},
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
