from icecream import ic as cout
import json


class SaveUtils:
    def __init__(self):
        pass

    def remove_saved_items(self, word: str):
        with open("DataStudio/saved.json", "r") as file:
            data = json.load(file)
            data.reverse()
        for _data_ in data:
            if _data_["word"] == word:
                data.remove(_data_)
                cout(_data_)

        # with open("DataStudio/saved.json", "w") as file:
        #     json.dump(data, file)

    def get_saved_items(self) -> list:
        with open("DataStudio/saved.json", "r") as file:
            data = json.load(file)
            data.reverse()

        return data
