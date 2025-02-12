import json


def get_file_list():
    try:
        files = json.load(open("included_files.json"))
    except FileNotFoundError:
        files = ["deities.json", "items.json"]
        json.dump(files, open("included_files.json", "w"))
    return files
