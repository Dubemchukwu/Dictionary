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
        with open("DataStudio/dic_words.txt", "r") as file:
            self.words = file.read().removesuffix("\n")
            self.words = self.words.split("\n")
        return self.words


class Daily_:
    def __init__(self):
        pass

    @staticmethod
    def get_state():
        try:
            with open("DataStudio/info.json", "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {"last_date": None, "quote_index": 0}

    @staticmethod
    def save_state(state):
        with open("DataStudio/info.json", "w") as file:
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
        if int(time.strftime("%d")) != int(data["date"]):
            Constants().set_daily_saved_state(False)

            bookmark_button = \
            screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                -2].content.controls[
                -1].content.controls[0].controls[-1]

            bookmark_button.selected = Constants().get_daily_saved_state()

            screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                -2].content.controls[
                -1].content.controls[0].controls[-1].update()

            data["date"] = int(time.strftime("%d"))
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
            # response.json()[0]["shortdef"][0]

            data["meaning"] = __temp

            # response.json()[0]["def"][0]["sseq"][1][0][1]["dt"][0][1].replace("{bc}",
            #                                                                                 "").replace(
            # "{", "").replace("}", "").replace("|", "")

            # cout(response.json()[0]["fl"], response.json()[0]["shortdef"], response.status_code)
            # cout(data)
            Daily_.save_state(data)

        else:
            cout("hello world!!!")

        # if isinstance(screen.views[-1].controls[0].content.data, Variable):
        #     screen.views[-1].controls[0].content.content.content.controls[3].content.controls[-2].content.controls[-1].content.controls[0]
        #     # screen.
        # except:
        #     cout("errors")

        # threading.Timer(60, ApiCont.daily_word_gen, kwargs={"screen":screen}).start()
        screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            -2].content.controls[
            -1].content.controls[0].controls[0].controls[1].value = data["word"]
        screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            -2].content.controls[
            -1].content.controls[0].controls[0].controls[2].value = data["pos"]
        screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            -2].content.controls[
            -1].content.controls[1].value = data["meaning"]
        screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            -2].content.controls[
            -1].content.controls[3].controls[0].value = time.strftime(f"%d{daily_word().suffix} %B, %Y")

        screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            -2].content.controls[
            -1].content.controls[0].controls[0].controls[1].update()
        screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            -2].content.controls[
            -1].content.controls[0].controls[0].controls[2].update()
        screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            -2].content.controls[
            -1].content.controls[1].update()
        screen.views[-1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            -2].content.controls[
            -1].content.controls[3].controls[0].update()

        # cout(Variable._daily_word)


class Constants:
    animated_switcher = Ref[AnimatedSwitcher]()
    searched_word = ""
    notify_search_loading = SnackBar(
        on_visible=lambda e: Constants.open_up_snack(e),
        bgcolor=Colors.TRANSPARENT,
        elevation=0, duration=5000,
        behavior=SnackBarBehavior.FIXED,
        dismiss_direction=DismissDirection.VERTICAL,
        content=Row(
            height=60,
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Container(
                    width=150, height=30,
                    scale=0, on_animation_end=lambda e: Constants.end_animation(e),
                    animate_scale=Animation(1500, AnimationCurve.ELASTIC_OUT),
                    animate=Animation(1000, AnimationCurve.ELASTIC_IN),
                    shadow=[BoxShadow(
                        spread_radius=1,
                        color=Colors.GREY,
                        offset=(0, 1),
                        blur_radius=1,
                    ),
                        BoxShadow(
                            spread_radius=1,
                            color=Colors.GREY,
                            offset=(0, 1),
                            blur_radius=1,
                        )
                    ],
                    border_radius=6,
                    alignment=alignment.center,
                    bgcolor=Colors.WHITE,
                    content=Text("Search is loading", size=13, text_align=TextAlign.CENTER, weight=FontWeight.W_600),
                ),
            ],
        ),
    )

    @staticmethod
    def open_up_snack(e: ControlEvent):
        e.control.content.controls[0].scale = 1.05
        e.control.content.controls[0].update()

    @staticmethod
    def end_animation(e: ControlEvent):
        e.control.scale = 1
        e.control.update()

    def __init__(self):
        pass

    def set_daily_saved_state(self, state: bool) -> None:
        data = dict()
        try:
            with open("DataStudio/constants.json", "r") as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError as error:
            pass
        finally:
            data["daily_saved_state"] = state

        with open("DataStudio/constants.json", "w") as file:
            json.dump(data, file)

    def get_daily_saved_state(self) -> bool:
        try:
            with open("DataStudio/constants.json", "r") as file:
                data = json.load(file)

            return data.get("daily_saved_state")

        except json.decoder.JSONDecodeError as error:
            return False

        except FileNotFoundError as error:
            with open("DataStudio/constants.json", "x") as file:
                ...
            return False

    def get_search_saved_state(self, word) -> bool:
        # checked: bool = False
        with open("DataStudio/saved.json", "r") as file:
            data = json.load(file)
        for block in data:
            if word in block.values():
                cout(word)
                return True
        return False


class Variable:
    see_all_state = False
    counts = 0

    def __init__(self):
        self.main_list = []
        self.remainder_list = []

    def save_search_bookmark(self):
        with open("DataStudio/saved.json", "r") as file:
            data: list = json.load(file)

        data.append(alt.search_result)

        with open("DataStudio/saved.json", "w") as file:
            json.dump(data, file)

    def delete_search_bookmark(self):
        with open("DataStudio/saved.json", "r") as file:
            data: list = json.load(file)

        for _ in data:
            if _.get("word") == alt.search_result.get("word"):
                data.remove(_)

                with open("DataStudio/saved.json", "w") as file:
                    json.dump(data, file)

    def _save_search(self, e: ControlEvent):
        if alt.to_save_state:
            cout(alt.search_result)
            e.control.rotate += math.pi * 2
            e.control.selected = True if e.control.selected == False else False
            e.control.update()
            if e.control.selected:
                self.save_search_bookmark()
            else:
                self.delete_search_bookmark()
        else:
            Constants.notify_search_loading.open = True
            Constants.notify_search_loading.update()
            cout("search can't be saved while, it's still loading")

    @staticmethod
    def delete_bookmark(data: dict):
        [data.pop(key) for key in ["date", "check"]]
        with open("DataStudio/saved.json", "r") as file:
            full_data: list = json.load(file)
        if data in full_data:
            full_data.remove(data)
        else:
            ...

        with open("DataStudio/saved.json", "w") as file:
            json.dump(full_data, file)

    @staticmethod
    def save_bookmark(data: dict):
        cout(data)
        [data.pop(key) for key in ["date", "check"]]
        full_data: list = []
        try:
            with open("DataStudio/saved.json", "r") as file:
                full_data: list = json.load(file)
        except:
            full_data: list = []

        finally:
            full_data.append(data)
            with open("DataStudio/saved.json", "w") as file:
                json.dump(full_data, file)

    def undo_refresh(self, e: ControlEvent):
        e.control.rotate -= math.pi * 2
        e.control.update()

    def refresh_all(self, e: ControlEvent):
        e.control.rotate += math.pi * 2
        e.control.update()

    def _refreshing_all(self, e: ControlEvent):
        e.page.views[1].controls[0].content = None
        e.page.views[1].controls[0].content = Home()._content_(e)
        e.page.views[1].controls[0].update()
        cout("refreshed")

    def create_history(self, wordz):
        with open("DataStudio/recent.rec", "a") as recent:
            recent.write(wordz + ",")

    def list_history(self):
        self.checking = 0
        with open("DataStudio/recent.rec", "r") as recent:
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
        e.control.scale = 1.25
        e.control.selected = True if e.control.selected == False else False
        e.control.update()
        Constants().set_daily_saved_state(e.control.selected)
        if e.control.selected:
            Variable.save_bookmark(Daily_.get_state())
        else:
            Variable.delete_bookmark(Daily_.get_state())

    def _end_save_(self, e: ControlEvent):
        e.control.scale = 1
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
                        color=Colors.BLACK,
                        width=450, height=250, fit=ImageFit.COVER,
                        border_radius=border_radius.all(20),
                    ),
                    Container(width=450, height=250, border_radius=20,
                              bgcolor=Colors.with_opacity(0.55, Colors.BLACK),
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
                                                    value="Word of the day", size=15,
                                                    font_family="league_light",
                                                    color=self.color,
                                                    style=TextStyle(
                                                        shadow=BoxShadow(spread_radius=8, blur_radius=1,
                                                                         blur_style=ShadowBlurStyle.OUTER,
                                                                         color=Colors.with_opacity(0.75,
                                                                                                   Colors.BLACK),
                                                                         offset=(0, .0023),
                                                                         ),
                                                        word_spacing=2),
                                                ),
                                                Text(
                                                    value=str(ApiCont().word).lower(), weight=FontWeight.W_900,
                                                    size=22, color=self.color,
                                                    style=TextStyle(
                                                        font_family="spartan_semi_bold",
                                                        shadow=BoxShadow(spread_radius=4, blur_radius=1,
                                                                         blur_style=ShadowBlurStyle.OUTER,
                                                                         color=Colors.with_opacity(0.5,
                                                                                                   Colors.BLACK),
                                                                         offset=(0, .0023),
                                                                         ),
                                                        letter_spacing=3,
                                                    ),
                                                ),
                                                Text(
                                                    value=ApiCont().POS, weight=FontWeight.NORMAL,
                                                    italic=True, size=13, color=self.color,
                                                    style=TextStyle(
                                                        font_family="roboto_mono_light",
                                                        shadow=BoxShadow(spread_radius=8, blur_radius=1,
                                                                         blur_style=ShadowBlurStyle.OUTER,
                                                                         color=Colors.with_opacity(0.75,
                                                                                                   Colors.BLACK),
                                                                         offset=(0, .0023),
                                                                         ), letter_spacing=1,
                                                    ),
                                                ),
                                            ],
                                        ),

                                        IconButton(
                                            icon=Icons.BOOKMARK_OUTLINE_ROUNDED,
                                            scale=1,
                                            selected=Constants().get_daily_saved_state(),
                                            icon_size=30, splash_radius=10,
                                            splash_color=Colors.WHITE,
                                            on_click=lambda e: self._save_(e),
                                            on_animation_end=lambda e: self._end_save_(e),
                                            animate_scale=animation.Animation(
                                                550,
                                                animation.AnimationCurve.ELASTIC_OUT),
                                            selected_icon=Icons.BOOKMARK_ROUNDED,
                                            icon_color=Colors.WHITE, selected_icon_color=Colors.WHITE,
                                            style=ButtonStyle(
                                                elevation=10,
                                                overlay_color=Colors.BLACK12,
                                                surface_tint_color=Colors.TRANSPARENT,
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
                                                         color=Colors.with_opacity(0.75,
                                                                                   Colors.BLACK),
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
                                                                 color=Colors.with_opacity(0.75,
                                                                                           Colors.BLACK),
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
            vertical_alignment=CrossAxisAlignment.END,
            spacing=1, run_spacing=1,
            controls=[
                Container(
                    padding=padding.only(left=0),
                    width=60,
                    alignment=alignment.center,
                    content=Text(
                        value=text_,
                        text_align=TextAlign.CENTER,
                        overflow=TextOverflow.ELLIPSIS,
                        font_family="spartan",
                        height=20,
                        width=60,
                        size=16,
                        color="#434343",
                    ),
                    on_click=lambda e: self.__search_word__(e),
                ),
                IconButton(
                    icon=Icons.CANCEL_OUTLINED,
                    scale=1.1,
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

    def __search_word__(self, e: ControlEvent):
        e.data = e.control.content.value
        Constants.searched_word = e.data
        e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[0].controls[
            1].value = e.data
        e.page.views[1].controls[0].content.content.content.controls[0].controls[3].data = "Search"
        saving = threading.Thread(target=Variable().create_history, kwargs={"wordz": e.data})

        e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[1].visible = True
        e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[1].update()

        e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content = SearchWidget(e)
        e.page.views[1].controls[0].content.content.content.controls[0].update()
        cout(e.data)

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

        # e.page.views[-1].controls[0].content.content.content.controls[3].content.controls[0].content.controls[2].controls.pop(
        #     e.control.data[1])
        #
        # e.page.views[-1].controls[0].content.content.content.controls[3].content.controls[0].content.controls[2].update()
        if Variable.see_all_state:
            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                0].content.controls[
                2].controls = Home()._add_history(
                Variable().list_history()[0] + Variable().list_history()[1],
            )
            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                0].content.controls[
                2].height = (38 * math.ceil(len(Variable().list_history()[0] + Variable().list_history()[1]) / 4))
            cout("Debug: deleting")
        else:
            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                0].content.controls[
                2].controls = Home()._add_history(
                Variable().list_history()[0],
            )

        e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            0].content.controls[2].update()
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
            e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[0].controls[
                0].value = ""
            # e.page.helper_text = ""
        else:
            e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[0].controls[
                0].value = word.lower()
            self.__complete_text = word.lower()
            cout(word.lower())
            # e.control.select_range(len(e.data), len(word))
        e.page.update()
        e.control.update()

    def __remove_label(self, e: ControlEvent):
        e.control.value = ""
        e.control.update()

    def __add_label_thread(self, e: ControlEvent):
        for i in "Type Here":
            e.control.value += i
            e.control.update()
            time.sleep(0.25)

    def __add_label(self, e: ControlEvent):
        if e.control.value == "" or e.control.value.lower == "type here":
            self.__add_label_thread(e)
        # self.label_thread = threading.Thread(target=self.__add_label_thread, kwargs={"e": e})
        # self.label_thread.start()

    def __search_word(self, e: ControlEvent):
        if e.data != "" or e.data.isspace() is False:
            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].data = "Search"
            saving = threading.Thread(target=Variable().create_history, kwargs={"wordz": e.data})
            saving.start()

            e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[
                1].selected = Constants().get_search_saved_state(e.data)
            e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[1].visible = True
            e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[1].update()

            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content = SearchWidget(e)
            e.page.views[1].controls[0].content.content.content.controls[0].update()
            cout(e.data)

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
            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                0].content.controls[
                2].height = (38 * math.ceil(len(Variable().list_history()[0] + Variable().list_history()[1]) / 4))

            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                0].content.controls[
                2].controls.extend(
                self._add_history(
                    Variable().list_history()[1],
                ))
            Variable.see_all_state = True
            e.control.text = "Shrink"

        else:
            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                0].content.controls[
                2].expand = False

            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                0].content.controls[
                2].height = 38

            e.control.text = "see all"
            e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                0].content.controls[
                2].controls = self._add_history(
                Variable().list_history()[0],
            )
            Variable.see_all_state = False

        cout(len(e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
                     0].content.controls[
                     2].controls))

        cout(e.data, "clicked")
        e.control.update()
        e.page.views[1].controls[0].content.content.content.controls[0].controls[3].content.controls[
            0].content.controls[2].update()
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
                            Text("Recently Searched", size=18, color="#000000", font_family="roboto"),
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
                                            bgcolor=Colors.WHITE,
                                            shape=BeveledRectangleBorder(1),
                                            overlay_color=Colors.TRANSPARENT,  # "#404040",
                                            surface_tint_color=Colors.BLACK,
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

    def __add_back_button(self, e: HoverEvent):
        if e.page.views[-1].controls[0].content.content.content.controls[0].controls[3].data != "Home":
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
        e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[1].visible = False
        e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[1].update()

        e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[0].controls[
            0].value = ""
        e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[0].controls[
            1].value = ""
        e.page.views[1].controls[0].content.content.content.controls[0].controls[2].controls[0].update()
        e.page.views[1].controls[0].content.content.content.controls[0].controls[3].data = "Home"
        e.page.views[-1].controls[0].content.content.content.controls[0].controls[3].content = self.content_home()
        e.page.views[-1].controls[0].content.content.content.controls[0].controls[3].update()
        if e.control.data == "left":
            e.control.offset = (-1.75, 0)
            e.control.update()
        else:
            e.control.offset = (1, 0)
            e.control.update()

    def change_screen(self, e: ControlEvent):
        if e.control.data == "saved":
            e.page.go("/saved")
            cout(e.page.route)
        elif e.control.data == "games":
            pass

    def _content_(self, e):
        return Container(
            data=Variable(),
            shadow=BoxShadow(spread_radius=8, blur_radius=1,
                             blur_style=ShadowBlurStyle.OUTER,
                             color=Colors.with_opacity(0.75,
                                                       Colors.BLACK),
                             offset=(0, .0023),
                             ),
            padding=padding.symmetric(0, 20),
            content=GestureDetector(
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
                                                    on_click=lambda e: Variable().refresh_all(e),
                                                    on_animation_end=lambda e: Variable()._refreshing_all(e),
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
                                            ],
                                        ),
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
                                                    cursor_color=Colors.BLACK,
                                                    selection_color="#606060",
                                                    text_style=TextStyle(
                                                        size=15, color="#666666",
                                                        font_family="roboto",
                                                        weight=FontWeight.W_600,
                                                    ),
                                                    border_radius=30, border=InputBorder.OUTLINE,
                                                    bgcolor="#d9d9d9",
                                                    border_color=Colors.BLACK, border_width=1,
                                                    # suffix_icon=Icons.SEARCH_ROUNDED,
                                                    suffix=Icon(
                                                        size=15, scale=1.9,
                                                        offset=(0, 0.1),
                                                        name=Icons.SEARCH_ROUNDED,
                                                        color=Colors.BLACK,
                                                    ),
                                                ),

                                                TextField(
                                                    on_blur=lambda e: self.__add_label(e),
                                                    on_focus=lambda e: self.__remove_label(e),
                                                    on_submit=lambda e: self.__search_word(e),
                                                    on_change=lambda e: self.__update_suggestions(e),
                                                    counter_style=TextStyle(
                                                        size=15, color="#666666",
                                                        font_family="roboto",
                                                    ), value="Type Here",
                                                    content_padding=padding.only(right=17.0, left=25.0),
                                                    width=360, hint_text="Type Here",
                                                    hint_style=TextStyle(
                                                        size=15, color="#666666",
                                                        font_family="roboto",
                                                    ), cursor_color=Colors.BLACK,
                                                    selection_color="#606060",
                                                    text_style=TextStyle(size=15, color=Colors.BLACK,
                                                                         weight=FontWeight.W_600, font_family="roboto"),
                                                    border_radius=30, border=InputBorder.OUTLINE,
                                                    bgcolor=Colors.with_opacity(0.012, "#d9d9d9"),
                                                    border_color=Colors.TRANSPARENT, border_width=1,
                                                    enable_suggestions=True, autocorrect=True,
                                                    # suffix_icon=Icons.SEARCH_ROUNDED,
                                                    suffix=Icon(
                                                        size=15, scale=1.9,
                                                        offset=(0, 0.1),
                                                        name=Icons.SEARCH_ROUNDED,
                                                        color=Colors.BLACK,
                                                    ),
                                                ),
                                            ],
                                        ),
                                        IconButton(
                                            icon=Icons.BOOKMARK_OUTLINE_ROUNDED,
                                            visible=False,
                                            scale=1, rotate=0,
                                            selected=Constants().get_search_saved_state(Constants.searched_word),
                                            icon_size=30, splash_radius=4,
                                            on_click=lambda e: Variable()._save_search(e),
                                            on_animation_end=lambda e: daily_word()._end_save_(e),
                                            animate_scale=animation.Animation(
                                                550,
                                                animation.AnimationCurve.ELASTIC_OUT),
                                            animate_rotation=animation.Animation(
                                                550,
                                                animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                            selected_icon=Icons.BOOKMARK_ROUNDED,
                                            icon_color=Colors.BLACK, selected_icon_color=Colors.BLACK54,
                                            splash_color=Colors.BLACK,
                                            style=ButtonStyle(
                                                bgcolor=Colors.TRANSPARENT,
                                                elevation=10,
                                                overlay_color=Colors.BLACK38,
                                                surface_tint_color=Colors.TRANSPARENT,
                                            ),
                                        ),
                                    ],
                                ),
                                AnimatedSwitcher(
                                    ref=Constants.animated_switcher,
                                    transition=AnimatedSwitcherTransition.FADE,
                                    height=550,
                                    data="Home",
                                    reverse_duration=250,
                                    duration=250, switch_in_curve=AnimationCurve.EASE_IN,
                                    switch_out_curve=AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED,
                                    content=self.content_home(),  # SearchWidget(e),
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

    def content(self):
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
