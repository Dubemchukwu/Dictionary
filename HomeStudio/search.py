import threading
import time
from cryptography.fernet import Fernet
from flet import *
from icecream import ic as cout
from google import generativeai as genai
import requests


def decrypt_api_key(key_file="HomeStudio/fernet.key"):
    with open("HomeStudio/.env", "rb") as file:
        encrypted_api_key = file.read()

    with open(key_file, "rb") as key_file:
        load_key = key_file.read()

    key = load_key
    fernet = Fernet(key)
    decrypted_api_key = fernet.decrypt(encrypted_api_key).decode()
    print(f"Decrypted API Key: {decrypted_api_key}")
    return decrypted_api_key

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# gemini-1.5-flash-latest
genai.configure(api_key=decrypt_api_key())
model = genai.GenerativeModel("gemini-2.0-flash-exp", safety_settings=False,
                              # generation_config=generation_config
                              )
AI = model.start_chat()


class VariableSearch:
    num_meanings = 0
    markdown = Ref[Markdown]()
    def __init__(self):
        pass


class MeaningWidget:
    def __init__(self, m_text: str, synonyms: str = "...", antonyms: str = "..."):
        self.meaning_text = m_text
        self.synonyms = synonyms
        self.antonyms = antonyms

    def build(self):
        VariableSearch.num_meanings += 1
        return Column(
            controls=[
                Text(
                    spans=[
                        TextSpan(
                            text=f"{VariableSearch.num_meanings}. ",
                            style=TextStyle(
                                font_family="lexend",
                                size=16, weight=FontWeight.W_600,
                                color=colors.ON_PRIMARY,
                            ),
                        ),
                        TextSpan(
                            text=f"{self.meaning_text}. ",
                            style=TextStyle(
                                font_family="lexend",
                                size=15, weight=FontWeight.W_600,
                                color=colors.ON_PRIMARY, word_spacing=0.25,
                            ),
                        ),
                    ],
                    text_align=TextAlign.LEFT,
                ),
                Container(
                    padding=padding.only(left=10),
                    content=Column(
                        controls=[
                            Text(
                                width=400,
                                overflow=TextOverflow.ELLIPSIS,
                                max_lines=1,
                                spans=[
                                    TextSpan(
                                        text="SYNONYMS: ",
                                        style=TextStyle(
                                            font_family="lexend_light",
                                            size=16, weight=FontWeight.W_500,
                                            color=colors.ON_PRIMARY,
                                        ),
                                    ),
                                    TextSpan(
                                        text=self.synonyms,
                                        style=TextStyle(
                                            overflow=TextOverflow.ELLIPSIS,
                                            font_family="lexend_semi_bold",
                                            size=14, weight=FontWeight.W_900,
                                            color="#1d3557",
                                        ),
                                    ),
                                ],
                            ),
                            Text(
                                spans=[
                                    TextSpan(
                                        text="ANTONYM: ",
                                        style=TextStyle(
                                            font_family="lexend_light",
                                            size=16, weight=FontWeight.W_500,
                                            color=colors.ON_PRIMARY,
                                        ),
                                    ),
                                    TextSpan(
                                        text=self.antonyms,
                                        style=TextStyle(
                                            font_family="lexend_semi_bold",
                                            size=14, weight=FontWeight.BOLD,
                                            color="#a92227",
                                        ),
                                    ),
                                ],
                            ), ],
                    ),
                ),
            ],
        )


class alt:
    to_save_state = False
    search_result = {}
    search_result_meaning = []

    search_column = Ref[Column]()

    @staticmethod
    def get_data():
        syno_first = alt.search_column.current.controls[-1].controls[1].content.controls[
                0].spans[
                1].text
        syno_sec = alt.search_column.current.controls[-2].controls[1].content.controls[
                0].spans[
                1].text

        anto_first = alt.search_column.current.controls[-1].controls[1].content.controls[
                1].spans[
                1].text
        anto_second = alt.search_column.current.controls[-2].controls[1].content.controls[
                1].spans[
                1].text

        first_meaning = alt.search_result_meaning[1]
        second_meaning = alt.search_result_meaning[0]

        searches = [
            {"meaning": first_meaning,
             "synonyms": syno_first,
             "antonyms": anto_first,
             },
            {"meaning": second_meaning,
             "synonyms": syno_sec,
             "antonyms": anto_second,
             },
        ]
        searches.reverse()
        alt.search_result["searches"] = searches

    def __init__(self):
        self.data = "insouciant"


class SearchWidget(Column):
    _state_ = True
    def __init__(self, e: ControlEvent = None):
        super().__init__()
        self.e = e or alt()
        self.__inc = 0
        self.__count = 0
        self.__check__ = False
        self.alignment = MainAxisAlignment.SPACE_EVENLY
        self.horizontal_alignment = CrossAxisAlignment.START
        self.spacing = 0
        self.run_spacing = 0
        self.scroll = ScrollMode.ALWAYS
        self.height = 550
        self.controls = [
            self._content_(),
        ]
        VariableSearch.num_meanings = 0
        cout(SearchWidget._state_,"searchWidget")
        if SearchWidget._state_:
            threading.Timer(interval=0, function=self._data_dict).start()

        self.__ai_resp = threading.Timer(interval=0, function=self.__ai_response)
        self.__ai_resp.start()

    def __ai_completion(self, position, meaning):
        self.temp_dict = {}
        try:
            self.__syno_ = AI.send_message(
                f"generate the synonym or synonyms (word) for the phrase or sentence {meaning} in a list, seperated by commas. Note: max of 3 or 2 words/synonyms.\
                Note: do not repeat any of the synonyms you've mentioned in the list or used before.")
            self.__anto_ = AI.send_message(
                f"generate the antonym (word) for the phrase or sentence {meaning}. \
                Note: do not repeat any of the antonym you've mentioned or used. \
                Note: i want only words in your response.",
            )
            self.controls[0].content.controls[1].controls[position].controls[1].content.controls[
                0].spans[
                1].text = self.__syno_.text.removesuffix("\n")
            self.controls[0].content.controls[1].controls[position].controls[1].content.controls[
                1].spans[
                1].text = self.__anto_.text.removesuffix("\n")
            # cout(self.__syno_.text, self.__anto_.text)

            self.controls[0].content.controls[1].controls[position].controls[1].content.update()

        except:
            while not self.__check__:
                pass
            time.sleep(1)
            self.__syno_ = AI.send_message(
                f"generate the synonym or synonyms (word) for the phrase or sentence {meaning} in a list, seperated by commas. Note: max of 3 or 2 words/synonyms.\
                            Note: do not repeat any of the synonyms you've mentioned in the list or used before.")
            self.__anto_ = AI.send_message(
                f"generate the antonym (word) for the phrase or sentence {meaning}. \
                            Note: do not repeat any of the antonym you've mentioned or used. \
                            Note: i want only words in your response.",
            )
            self.controls[0].content.controls[1].controls[position].controls[1].content.controls[
                0].spans[
                1].text = self.__syno_.text.removesuffix("\n")
            self.controls[0].content.controls[1].controls[position].controls[1].content.controls[
                1].spans[
                1].text = self.__anto_.text.removesuffix("\n")
            # cout(self.__syno_.text, self.__anto_.text)

            self.controls[0].content.controls[1].controls[position].controls[1].content.update()

            # self.temp_dict["meaning"] = str(meaning).capitalize()
            # self.temp_dict["synonyms"] = \
            #     self.controls[0].content.controls[1].controls[position].controls[1].content.controls[
            #         0].spans[
            #         1].text
            # self.temp_dict["antonym"] = \
            #     self.controls[0].content.controls[1].controls[position].controls[1].content.controls[
            #         1].spans[
            #         1].text

        finally:
            # self.controls[0].content.controls[1].controls[position].controls[1].content.update()
            # alt.search_result["searches"][position] = self.temp_dict
            # if position == -1:
            #     alt.search_result_1 = self.temp_dict
            # if position == -2:
            #     alt.search_result_2 = self.temp_dict

            # cout(alt.search_result["searches"])

            self.__count += 1
            if self.__count == 2 and \
                    self.controls[0].content.controls[1].controls[position].controls[1].content.controls[
                        1].spans[
                        1].text != "...":
                # cout(alt.search_result_2, alt.search_result_1)
                cout("you can save now", self.__count)
                # self.temp_dict_2 = {"meaning", "synonyms", "antonym"}
                # self.temp_dict_1 = {}
                alt.get_data()
                alt.to_save_state = True
                if self.controls[0].content.controls[1].controls[1].data == "loading":
                    self.controls[0].content.controls[1].controls[1].visible = False
                else:
                    pass
                self.controls[0].content.controls[1].update()
                self.__count = 0


    def _data_dict(self):
        alt.search_result_meaning.clear()
        self.__meaning_word_1 = AI.send_message(
            f"two meanings of the word '{self.e.data}'. A short precise answer or meaning to the word, only one or two sentences. Note: it should be seperated by ':' to indicate to different meanings. ")

        self.__reply_dict = requests.get(
            f"https://dictionaryapi.com/api/v3/references/sd4/json/{self.e.data}?key=166e17cb-08dd-4439-a142-85763906e46d",
        )
        # cout(self.__meaning_word_1.text)
        self.__list_meaning = self.__meaning_word_1.text.split(":")
        if int(self.__reply_dict.status_code) == 200:
            try:
                self.controls[0].content.controls[1].controls[0].spans[1].text = \
                    self.__reply_dict.json()[0].get("fl")
            except:
                self.controls[0].content.controls[1].controls[0].spans[1].text = \
                    "i don't know, honestly"
            alt.search_result["word"] = self.e.data
            alt.search_result["pos"] = self.controls[0].content.controls[1].controls[0].spans[1].text
            alt.search_result["searches"] = []
            for _text_ in self.__list_meaning:
                _text_ = _text_.replace("\n", "").replace(".", "")
                while _text_.startswith(" "):
                    _text_ = _text_.removeprefix(" ")

                self.__inc -= 1
                alt.search_result_meaning.append(_text_)
                self.controls[0].content.controls[1].controls.append(
                    MeaningWidget(m_text=str(_text_).capitalize()).build(),
                )

                # self.__ai_completion(-1, _text_)
                threading.Thread(target=self.__ai_completion,
                                 kwargs={"position": self.__inc, "meaning": _text_}).start()
        # self.controls[0].content.controls[1].controls[self.__inc].controls[1].content.update()
        self.controls[0].content.controls[1].update()
        # cout(self.__reply_dict.json(), self.__reply_dict.json()[0]["fl"], self.__list_meaning)

    def __ai_response(self):
        try:
            self.__value = ""
            self.response = AI.send_message(f"Shed more insight's on the word " + f'"{self.e.data}"', stream=True)
            for chunk in self.response:
                self.__value += chunk.text
                self.controls[0].content.controls[3].controls[1].content.controls[0].value = self.__value
                self.controls[0].content.controls[3].controls[1].content.controls[0].update()
                # return self.__value
            self.__check__ = True
        except:
            self.controls[0].content.controls[3].controls[1].content.controls[0].value = ""
            self.controls[0].content.controls[3].controls[1].content.controls[0].update()


    def _content_(self):
        return Container(
            padding=padding.all(0),
            alignment=alignment.top_left,
            data="markdown_parent",
            content=Column(
                spacing=10, run_spacing=10,
                controls=[
                    Text(
                        value=self.e.data,
                        style=TextStyle(
                            font_family="lexend",
                            size=24, weight=FontWeight.W_800,
                            color=colors.ON_PRIMARY,
                        ),
                    ),
                    Column(
                        spacing=20, run_spacing=20,
                        ref=alt.search_column,
                        controls=[
                            Text(
                                style=TextStyle(
                                    word_spacing=0.05,
                                ),
                                spans=[
                                    TextSpan(
                                        "Part of Speech: ",
                                        style=TextStyle(
                                            word_spacing=0.05,
                                            font_family="roboto_medium",
                                            size=17, weight=FontWeight.W_700,
                                            color=colors.ON_PRIMARY,
                                        ),
                                    ),
                                    TextSpan(
                                        "",
                                        style=TextStyle(
                                            font_family="roboto_mono",
                                            italic=True,
                                            size=18, weight=FontWeight.W_400,
                                            color="#a92227",
                                        ),
                                    )
                                ],
                            ),
                            Row(
                                data="loading",
                                alignment=MainAxisAlignment.CENTER,
                                controls=[ProgressRing(
                                    color=colors.ON_PRIMARY,
                                    stroke_width=7,
                                    stroke_cap=StrokeCap.ROUND,
                                    width=50,
                                    height=50,
                                )],
                            ),
                            # MeaningWidget(m_text="Increase rapidly",
                            #               antonyms="plunge",
                            #               synonyms="rocket, soar, spiral , surge, climb").build(),
                            # MeaningWidget(m_text="Make or become more intense or serious",
                            #               antonyms="shrink",
                            #               synonyms="rocket, soar, spiral , surge, climb").build(),
                        ],
                    ),

                    TransparentPointer(height=30),
                    Column(
                        alignment=MainAxisAlignment.START,
                        spacing=15, run_spacing=15,
                        controls=[
                            Container(
                                height=50, width=460,
                                border_radius=border_radius.all(15),
                                bgcolor=Colors.ON_SECONDARY_CONTAINER,
                                padding=padding.only(left=10, right=10),
                                content=Row(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Text(
                                            value=f"Shed insight's on the word " + f'"{self.e.data}"',
                                            style=TextStyle(
                                                font_family="lexend_light",
                                                size=15, weight=FontWeight.W_400,
                                                color=colors.ON_PRIMARY,
                                            ),
                                        ),
                                        Icon(
                                            name=icons.WIDGETS,
                                        ),
                                    ],
                                ),
                            ),
                            Container(
                                width=460, height=250,
                                border_radius=border_radius.all(15),
                                bgcolor=Colors.ON_SECONDARY_CONTAINER,
                                padding=padding.only(left=15, top=15, bottom=15, right=15),
                                content=Column(
                                    scroll=ScrollMode.ALWAYS,
                                    alignment=MainAxisAlignment.START,
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Markdown(
                                            ref=VariableSearch.markdown,
                                            value="",
                                            code_theme=MarkdownCodeTheme.LIGHTFAIR,
                                            md_style_sheet=MarkdownStyleSheet(
                                                em_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ),
                                                p_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ),
                                                a_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ),
                                                list_bullet_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ),
                                                blockquote_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ),
                                                checkbox_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ),
                                                code_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ),
                                                strong_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), h1_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), h2_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), h3_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), h4_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), del_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), img_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), h5_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), h6_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), table_head_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ), table_body_text_style=TextStyle(
                                                    font_family="lexend_light",
                                                    size=15, weight=FontWeight.W_400,
                                                    color=colors.ON_PRIMARY,
                                                ),
                                            ), width=450,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                    TransparentPointer(height=15),
                ],
            ),
        )


"""
If the object is very far away (e.g., in the upper atmosphere), its angular velocity in the field of view would decrease, making it appear slower. However, at typical observation distances, it would still be far too fast for the human eye to follow.
                                            The human eye processes information at roughly 60 frames per second, or every ~16 milliseconds. An object moving at Mach 27 could cover significant distances (e.g., kilometers) in that time, resulting in a blur or no visible trace.
                                            At speeds like Mach 27, an object would generate intense heat and potentially a plasma trail (e.g., meteors or spacecraft re-entering Earth's atmosphere). The eye would see the glowing trail left behind rather than the object itself.
                                            With specialized high-speed cameras or radar systems, it's possible to capture or track such fast-moving objects. However, the unaided human eye is not capable of following them in real-time.
                                            In conclusion: No, your eye cannot follow an object moving at Mach 27, though you might see its effects (like a glowing trail or shockwave)."""
