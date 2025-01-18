import json
from decorator import decorator_func
import urllib.parse


@decorator_func
def saver_to_json(data):
    parse_data = urllib.parse.unquote_plus(data)
    data_dict = {key: value for key, value in
                 [el.split("=") for el in parse_data.split("&")]}
    with open("storage/data.json", "w", encoding="utf-8") as file:
        json.dump(data_dict, file, ensure_ascii=False, indent=4)

    return data_dict
