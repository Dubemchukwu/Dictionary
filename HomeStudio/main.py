import json
import math
import random
import threading
import time
from HomeStudio.search import *
import english_words
# from nltk.corpus import words
from english_words import get_english_words_set

words = get_english_words_set(["web2"], alpha=True)


class Words:
    def __init__(self):
        self.words = None

    def init(self):
        with open("dic_words.txt", "r") as file:
            self.words = file.read().removesuffix("\n")
            self.words = self.words.split("\n")
        return self.words


class Daily_:
    def __init__(self):
        pass

    @staticmethod
    def get_state():
        try:
            with open("info.json", "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {"last_date": None, "quote_index": 0}

    @staticmethod
    def save_state(state):
        with open("info.json", "w") as file:
            json.dump(state, file)


class ApiCont:
    def __init__(self):
        data = Daily_.get_state()
        self.word = data["word"]
        self.POS = data["pos"]
        self.meaning = data["meaning"]

    @staticmethod
    def daily_word_gen(screen: Page):
        __temp = ""
        data = Daily_.get_state()
        if int(time.strftime("%d")) == data["date"]:
            # data["date"] = int(time.strftime("%d"))
            word_ = random.choice(list(Words().init()))
            cout(word_)
            response = requests.get(
                f"https://dictionaryapi.com/api/v3/references/sd4/json/{word_}?key=166e17cb-08dd-4439-a142"
                f"-85763906e46d",
            )

            data["pos"] = response.json()[0]["fl"]
            data["word"] = word_
            for def_ in response.json()[0]["shortdef"]:
                if len(def_) > len(__temp):
                    __temp = def_

            data["meaning"] = response.json()[0]["shortdef"][0]

            # response.json()[0]["def"][0]["sseq"][1][0][1]["dt"][0][1].replace("{bc}",
            #                                                                                 "").replace(
            # "{", "").replace("}", "").replace("|", "")

            cout(response.json())
            cout(response.json()[0]["fl"], response.json()[0]["shortdef"], response.status_code)
            cout(data)
            Daily_.save_state(data)

        else:
            cout("hello world!!!")

        # if isinstance(screen.views[-1].controls[0].content.data, Variable):
        #     screen.views[-1].controls[0].content.content.controls[3].content.controls[-2].content.controls[-1].content.controls[0]
        #     # screen.
        # except:
        #     cout("errors")

        # threading.Timer(60, ApiCont.daily_word_gen, kwargs={"screen":screen}).start()

        screen.views[-1].controls[0].content.content.controls[3].content.controls[-2].content.controls[
            -1].content.controls[0].controls[0].controls[1].value = data["word"]
        screen.views[-1].controls[0].content.content.controls[3].content.controls[-2].content.controls[
            -1].content.controls[0].controls[0].controls[2].value = data["pos"]
        screen.views[-1].controls[0].content.content.controls[3].content.controls[-2].content.controls[
            -1].content.controls[1].value = data["meaning"]
        screen.views[-1].controls[0].content.content.controls[3].content.controls[-2].content.controls[
            -1].content.controls[3].controls[0].value = time.strftime(f"%d{daily_word().suffix} %B, %Y")

        screen.views[-1].controls[0].content.content.controls[3].content.controls[-2].content.controls[
            -1].content.controls[0].controls[0].controls[1].update()
        screen.views[-1].controls[0].content.content.controls[3].content.controls[-2].content.controls[
            -1].content.controls[0].controls[0].controls[2].update()
        screen.views[-1].controls[0].content.content.controls[3].content.controls[-2].content.controls[
            -1].content.controls[1].update()
        screen.views[-1].controls[0].content.content.controls[3].content.controls[-2].content.controls[
            -1].content.controls[3].controls[0].update()

        # cout(Variable._daily_word)


class Variable:
    see_all_state = False
    counts = 0

    def __init__(self):
        self.main_list = []
        self.remainder_list = []

    def refresh_all(self, e: ControlEvent):
        e.control.rotate = e.control.rotate + math.pi * 2
        e.control.update()

    def _refreshing_all(self, e: ControlEvent):
        e.page.views[1].controls[0].content = None
        e.page.views[1].controls[0].content = Home()._content_()
        e.page.views[1].controls[0].update()
        cout("refreshed")

    def create_history(self, wordz):
        with open("recent.rec", "a") as recent:
            recent.write(wordz + ",")

    def list_history(self):
        self.checking = 0
        with open("recent.rec", "r") as recent:
            wordz = recent.read()[:-1]
            wordz = wordz.split(",")

            for word in reversed(wordz):
                if self.checking <= 3:
                    self.main_list.append(word)
                else:
                    self.remainder_list.append(word)
                self.checking += 1

        return [self.main_list, self.remainder_list]


# this is the daily word content
class daily_word:
    def __init__(self):
        self.color = "#d9d9d9"
        day = int(time.strftime("%d"))
        if 10 <= day % 100 <= 20:
            self.suffix = "th"
        else:
            self.suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        self.choice = random.randint(1, 500)
        # while True:
        #     day = int(time.strftime("%d"))
        #     if 10 <= day % 100 <= 20:
        #         suffix = "th"
        #     else:
        #         suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        #     self._build().content.controls[1].content.controls[3].controls[0].value = time.strftime(f"%d{suffix} %B, %Y")

    def _save_(self, e: ControlEvent):
        if e.control.rotate > math.pi:
            e.control.rotate = 0
        else:
            e.control.rotate = math.pi * 2
        e.control.selected = True if e.control.selected == False else False
        e.control.update()

    def _end_save_(self, e: ControlEvent):
        # e.control.rotate = math.pi
        e.control.update()

    def _build(self):
        return Container(
            margin=margin.only(top=0),
            alignment=alignment.top_center,
            content=Stack(
                controls=[
                    Image(
                        filter_quality=FilterQuality.LOW,
                        src=f"https://picsum.photos/id/{self.choice}/450/250",
                        color_blend_mode=BlendMode.DST_IN,
                        color=colors.BLACK,
                        width=450, height=250, fit=ImageFit.COVER,
                        border_radius=border_radius.all(20),
                    ),
                    Container(width=450, height=250, border_radius=20,
                              bgcolor=colors.with_opacity(0.55, colors.BLACK),
                              alignment=alignment.center_left,
                              ),
                    Container(
                        width=450, height=250, border_radius=20,
                        alignment=alignment.center_left,
                        padding=padding.symmetric(0, 20),
                        content=Column(
                            alignment=MainAxisAlignment.SPACE_EVENLY,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        Column(
                                            height=90,
                                            alignment=MainAxisAlignment.SPACE_EVENLY,
                                            horizontal_alignment=CrossAxisAlignment.START,
                                            controls=[
                                                Text(
                                                    value="Word of the day", size=14,
                                                    font_family="league_light",
                                                    color=self.color,
                                                    style=TextStyle(
                                                        shadow=BoxShadow(spread_radius=8, blur_radius=1,
                                                                         blur_style=ShadowBlurStyle.OUTER,
                                                                         color=colors.with_opacity(0.75,
                                                                                                   colors.BLACK),
                                                                         offset=(0, .0023),
                                                                         ),
                                                        word_spacing=2),
                                                ),
                                                Text(
                                                    value=ApiCont().word, weight=FontWeight.W_900,
                                                    size=20, color=self.color,
                                                    style=TextStyle(
                                                        shadow=BoxShadow(spread_radius=4, blur_radius=1,
                                                                         blur_style=ShadowBlurStyle.OUTER,
                                                                         color=colors.with_opacity(0.5,
                                                                                                   colors.BLACK),
                                                                         offset=(0, .0023),
                                                                         ),
                                                        letter_spacing=3,
                                                    ),
                                                ),
                                                Text(
                                                    value=ApiCont().POS, weight=FontWeight.NORMAL,
                                                    italic=True, size=11, color=self.color,
                                                    style=TextStyle(
                                                        shadow=BoxShadow(spread_radius=8, blur_radius=1,
                                                                         blur_style=ShadowBlurStyle.OUTER,
                                                                         color=colors.with_opacity(0.75,
                                                                                                   colors.BLACK),
                                                                         offset=(0, .0023),
                                                                         ), letter_spacing=1,
                                                    ),
                                                ),
                                            ],
                                        ),

                                        IconButton(
                                            icon=icons.BOOKMARK_OUTLINE_ROUNDED,
                                            rotate=0,
                                            icon_size=30, splash_radius=10,
                                            on_click=lambda e: self._save_(e),
                                            on_animation_end=lambda e: self._end_save_(e),
                                            animate_rotation=animation.Animation(
                                                750,
                                                animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                            selected_icon=icons.BOOKMARK_ROUNDED,
                                            icon_color=colors.WHITE, selected_icon_color=colors.WHITE,
                                            splash_color=colors.WHITE,
                                            style=ButtonStyle(
                                                elevation=10,
                                                overlay_color=colors.BLACK12,
                                                surface_tint_color=colors.TRANSPARENT,
                                            ),
                                        ),
                                    ],
                                ),
                                Text(
                                    value=ApiCont().meaning, overflow=TextOverflow.ELLIPSIS,
                                    max_lines=4,
                                    weight=FontWeight.W_500, size=14, color=self.color,
                                    style=TextStyle(
                                        shadow=BoxShadow(spread_radius=8, blur_radius=1,
                                                         blur_style=ShadowBlurStyle.OUTER,
                                                         color=colors.with_opacity(0.75,
                                                                                   colors.BLACK),
                                                         offset=(0, .0023),
                                                         ), letter_spacing=0.5,
                                    ),
                                ),
                                TransparentPointer(height=40),
                                Row(
                                    alignment=MainAxisAlignment.END,
                                    controls=[
                                        Text(
                                            value=time.strftime(f"%d{self.suffix} %B, %Y"),
                                            color=self.color,
                                            style=TextStyle(
                                                shadow=BoxShadow(spread_radius=8, blur_radius=1,
                                                                 blur_style=ShadowBlurStyle.OUTER,
                                                                 color=colors.with_opacity(0.75,
                                                                                           colors.BLACK),
                                                                 offset=(0, .0023),
                                                                 ),
                                                word_spacing=2),
                                            size=17,
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )


class history(Container):
    def __init__(self, text_: str):
        super().__init__()
        self.alignment = alignment.center
        self.content = Row(
            width=83,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            spacing=1, run_spacing=1,
            controls=[
                Container(
                    padding=padding.only(left=3),
                    width=60,
                    alignment=alignment.center,
                    content=Text(
                        value=text_,
                        overflow=TextOverflow.ELLIPSIS,
                        width=60,
                        size=13,
                        color="#434343",
                    ),
                    # on_click=lambda e: se
                ),
                IconButton(
                    icon=icons.CANCEL_OUTLINED,
                    data=[text_, Variable.counts],
                    on_click=lambda e: self.__delete(e),
                    icon_color="#1b1b1b",
                    icon_size=15,
                )
            ],
        )
        self.width = 103
        self.height = 30
        self.border_radius = border_radius.all(20)
        self.bgcolor = "#d9d9d9"
        Variable.counts += 1

    def __delete(self, e: ControlEvent):
        with open("recent.rec", "r") as file:
            file_data = file.read()
            file_data = file_data.replace(e.control.data[0] + ",", "")

        with open("recent.rec", "w") as file:
            file.write(file_data)
            cout(file_data)

        self.visible = False
        self.update()

        print(e.control.data[1])
        Variable.counts = 0

        # e.page.views[-1].controls[0].content.content.controls[3].content.controls[0].content.controls[2].controls.pop(
        #     e.control.data[1])
        #
        # e.page.views[-1].controls[0].content.content.controls[3].content.controls[0].content.controls[2].update()
        if Variable.see_all_state:
            e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[
                2].controls = Home()._add_history(
                Variable().list_history()[0] + Variable().list_history()[1],
            )
            e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[
                2].height = (38 * math.ceil(len(Variable().list_history()[0] + Variable().list_history()[1]) / 4))
            cout("Debug: deleting")
        else:
            e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[
                2].controls = Home()._add_history(
                Variable().list_history()[0],
            )

        e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[2].update()
        cout("deleted successfully")


class Home:
    def __init__(self):
        self.__complete_text = ""

    def __update_suggestions(self, e: ControlEvent):
        # cout(e.data)
        word = 40 * "."
        # print(word)
        # filtered_suggestions.controls.clear()

        matches = [word for word in words if word.lower().startswith(e.data.lower())]
        for match in matches:
            if len(match) < len(word):
                word = match

        if "." in word or len(word) == 1:
            e.page.views[1].controls[0].content.content.controls[2].controls[0].controls[0].value = ""
            # e.page.helper_text = ""
        else:
            e.page.views[1].controls[0].content.content.controls[2].controls[0].controls[0].value = word.lower()
            self.__complete_text = word.lower()
            cout(word.lower())
            # e.control.select_range(len(e.data), len(word))
        e.page.update()
        e.control.update()

    def __search_word(self, e: ControlEvent):
        if e.data != "" or e.data.isspace() is False:
            saving = threading.Thread(target=Variable().create_history, kwargs={"wordz": e.data})
            saving.start()

            e.page.views[1].controls[0].content.content.controls[2].controls[1].visible = True
            e.page.views[1].controls[0].content.content.controls[2].controls[1].update()

            e.page.views[1].controls[0].content.content.controls[3].content = SearchWidget(e)
            e.page.views[1].controls[0].content.content.update()
            cout(e.data)

    def add_suggestions(self, e: ControlEvent):
        e.control.value = self.__complete_text
        e.control.update()

    def _add_history(self, array):
        controls = []
        for word_ in array:
            if len(word_) == 0:
                pass
            else:
                self.__history_ = history(word_)
                controls.append(self.__history_)

        return controls

    def __expand_hist(self, e: ControlEvent):
        if e.control.text == "see all":
            e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[
                2].height = (38 * math.ceil(len(Variable().list_history()[0] + Variable().list_history()[1]) / 4))

            e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[
                2].controls.extend(
                self._add_history(
                    Variable().list_history()[1],
                ))
            Variable.see_all_state = True
            e.control.text = "Shrink"

        else:
            e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[
                2].expand = False

            e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[
                2].height = 38

            e.control.text = "see all"
            e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[
                2].controls = self._add_history(
                Variable().list_history()[0],
            )
            Variable.see_all_state = False

        cout(len(e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[
                     2].controls))

        cout(e.data, "clicked")
        e.control.update()
        e.page.views[1].controls[0].content.content.controls[3].content.controls[0].content.controls[2].update()
        cout(Variable.see_all_state)

    def content_home(self):
        return Column(
            alignment=MainAxisAlignment.SPACE_EVENLY,
            spacing=0, run_spacing=0, tight=True,
            height=430,
            controls=[
                Container(
                    padding=padding.only(left=10, top=10),
                    content=Column(
                        alignment=MainAxisAlignment.SPACE_EVENLY,
                        spacing=0, run_spacing=0, tight=True,
                        # height=100,
                        controls=[
                            Text("Recently Searched", size=15, color="#808080", font_family="roboto_light"),
                            TransparentPointer(height=10),
                            GridView(
                                animate_size=animation.Animation(750,
                                                                 AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN),
                                child_aspect_ratio=3.55, runs_count=4,
                                horizontal=False,
                                # alignment=MainAxisAlignment.START,
                                # scroll=ScrollMode.AUTO,
                                # auto_scroll=True,
                                width=460,
                                # vertical_alignment=CrossAxisAlignment.CENTER,
                                controls=self._add_history(Variable().list_history()[0]),
                            ),
                            Row(
                                alignment=MainAxisAlignment.END,
                                spacing=0, run_spacing=0,
                                controls=[
                                    TextButton(
                                        height=40,
                                        text="see all",
                                        on_click=lambda e: self.__expand_hist(e),
                                        style=ButtonStyle(
                                            color={ControlState.DEFAULT: "#292929",
                                                   ControlState.HOVERED: "#d9d9d9",
                                                   ControlState.PRESSED: "#404040"},
                                            bgcolor=colors.WHITE,
                                            shape=BeveledRectangleBorder(1),
                                            overlay_color=colors.TRANSPARENT,  # "#404040",
                                            surface_tint_color=colors.BLACK,
                                        ),
                                    )
                                ]
                            )
                        ],
                    ),
                ),
                daily_word()._build(),
                TransparentPointer(height=60)
            ],
        )

    def _content_(self):
        return Container(
            data=Variable(),
            shadow=BoxShadow(spread_radius=8, blur_radius=1,
                             blur_style=ShadowBlurStyle.OUTER,
                             color=colors.with_opacity(0.75,
                                                       colors.BLACK),
                             offset=(0, .0023),
                             ),
            padding=padding.symmetric(0, 20),
            content=Column(
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
                                             style=TextStyle(color=colors.BLACK),
                                             ),
                                    TextSpan("o",
                                             style=TextStyle(color="#9d0208"),
                                             ),
                                    TextSpan("nary",
                                             style=TextStyle(color=colors.BLACK),
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
                                        icon=icons.REFRESH_ROUNDED,
                                        rotate=0,
                                        style=ButtonStyle(
                                            bgcolor=colors.TRANSPARENT,
                                            overlay_color={ControlState.DEFAULT: colors.BLACK12,
                                                           ControlState.PRESSED: colors.BLACK12,
                                                           ControlState.HOVERED: colors.TRANSPARENT,
                                                           },
                                        ),
                                        animate_rotation=animation.Animation(
                                            1500,
                                            AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                        on_click=lambda e: Variable().refresh_all(e),
                                        on_animation_end=lambda e: Variable()._refreshing_all(e),
                                        icon_size=30,
                                        icon_color=colors.BLACK,
                                    ),
                                    IconButton(
                                        icon=icons.MORE_HORIZ_ROUNDED,
                                        style=ButtonStyle(
                                            bgcolor=colors.TRANSPARENT,
                                            overlay_color={ControlState.DEFAULT: colors.BLACK12,
                                                           ControlState.PRESSED: colors.BLACK12,
                                                           ControlState.HOVERED: colors.TRANSPARENT,
                                                           },
                                        ),
                                        icon_size=30,
                                        icon_color=colors.BLACK,
                                    ),
                                ]
                            )
                        ],
                    ),
                    TransparentPointer(height=35),
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Stack(
                                alignment=alignment.center,
                                controls=[
                                    TextField(
                                        counter_style=TextStyle(
                                            size=15, color="#666666",
                                            font_family="roboto"
                                        ),
                                        content_padding=padding.only(right=17.0, left=25.0),
                                        width=360,
                                        cursor_color=colors.BLACK,
                                        selection_color="#606060",
                                        text_style=TextStyle(
                                            size=15, color="#666666",
                                            font_family="roboto",
                                            weight=FontWeight.W_600,
                                        ),
                                        border_radius=30, border=InputBorder.OUTLINE,
                                        bgcolor="#d9d9d9",
                                        border_color=colors.BLACK, border_width=1,
                                        # suffix_icon=icons.SEARCH_ROUNDED,
                                        suffix=Icon(
                                            size=15, scale=1.9,
                                            offset=(0, 0.1),
                                            name=icons.SEARCH_ROUNDED,
                                            color=colors.BLACK,
                                        ),
                                    ),

                                    TextField(
                                        on_submit=lambda e: self.__search_word(e),
                                        on_change=lambda e: self.__update_suggestions(e),
                                        on_blur=lambda e: self.add_suggestions(e),
                                        counter_style=TextStyle(
                                            size=15, color="#666666",
                                            font_family="roboto"
                                        ),
                                        content_padding=padding.only(right=17.0, left=25.0),
                                        width=360, hint_text="Type Here",
                                        hint_style=TextStyle(
                                            size=15, color="#666666",
                                            font_family="roboto",
                                        ), cursor_color=colors.BLACK,
                                        selection_color="#606060",
                                        text_style=TextStyle(size=15, color=colors.BLACK,
                                                             weight=FontWeight.W_600, font_family="roboto"),
                                        border_radius=30, border=InputBorder.OUTLINE,
                                        bgcolor=colors.with_opacity(0.012, "#d9d9d9"),
                                        border_color=colors.TRANSPARENT, border_width=1,
                                        enable_suggestions=True, autocorrect=True,
                                        # suffix_icon=icons.SEARCH_ROUNDED,
                                        suffix=Icon(
                                            size=15, scale=1.9,
                                            offset=(0, 0.1),
                                            name=icons.SEARCH_ROUNDED,
                                            color=colors.BLACK,
                                        ),
                                    ),
                                ],
                            ),
                            IconButton(
                                icon=icons.BOOKMARK_OUTLINE_ROUNDED,
                                visible=False,
                                rotate=0,
                                icon_size=30, splash_radius=4,
                                on_click=lambda e: daily_word()._save_(e),
                                on_animation_end=lambda e: daily_word()._end_save_(e),
                                animate_rotation=animation.Animation(
                                    750,
                                    animation.AnimationCurve.ELASTIC_IN_OUT),
                                selected_icon=icons.BOOKMARK_ROUNDED,
                                icon_color=colors.BLACK, selected_icon_color=colors.BLACK54,
                                splash_color=colors.BLACK,
                                style=ButtonStyle(
                                    bgcolor=colors.TRANSPARENT,
                                    elevation=10,
                                    overlay_color=colors.BLACK38,
                                    surface_tint_color=colors.TRANSPARENT,
                                ),
                            ),
                        ],
                    ),
                    AnimatedSwitcher(
                        transition=AnimatedSwitcherTransition.SCALE,
                        height=550,
                        reverse_duration=750,
                        duration=1000, switch_in_curve=AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED,
                        switch_out_curve=AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED,
                        content=SearchWidget(None), #self.content_home(),
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text(
                                spans=[
                                    TextSpan(
                                        text="©",
                                        style=TextStyle(
                                            weight=FontWeight.W_500, color=colors.BLACK,
                                            size=17,
                                            shadow=BoxShadow(spread_radius=8, blur_radius=1,
                                                             blur_style=ShadowBlurStyle.OUTER,
                                                             color=colors.with_opacity(0.75,
                                                                                       colors.BLACK),
                                                             offset=(0, .0023),
                                                             ),
                                        ),
                                    ),
                                    TextSpan(
                                        text="NH-CEN Group4 PROJECT",
                                        style=TextStyle(
                                            weight=FontWeight.W_500, color=colors.BLACK,
                                            size=12,
                                            shadow=BoxShadow(spread_radius=0, blur_radius=0,
                                                             blur_style=ShadowBlurStyle.OUTER,
                                                             color=colors.with_opacity(0.75,
                                                                                       colors.BLACK),
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
        )
