import json
from typing import Literal
from cli import app
import inflect
from enum import StrEnum

from cli.utils import get_file_list

engine = inflect.engine()


class FormatEnum(StrEnum):
    list = "list"
    object = "object"

    @property
    def expected_type(self):
        if self == "object":
            return dict
        elif self == "list":
            return list
        else:
            return None


def objectify_list(data: list, singular: str):
    return {
        obj[f"{singular}_name"]: {
            k.replace(f"{singular}_", ""): v
            for k, v in obj.items()
            if k != f"{singular}_name"
        }
        for obj in data
    }


def listify_object(data: dict, singular: str):
    return [
        (
            {f"{singular}_name": key}
            | {
                f"{singular}_description" if k == "description" else k: v
                for k, v in value.items()
            }
        )
        for key, value in data.items()
    ]


@app.command()
def normalize(format: FormatEnum = FormatEnum.list):
    """
    Normalizes all included JSON files to follow the same format, based on the format argument

    list (Default):
        Normalizes the files to be a list of objects, with {subject}_name and {subject}_description keys, along with any other data
    object:
        Normalizes the files to be an object, with the keys being the names of the subject and each having a description key, along with any other data
    """
    files = get_file_list()
    for file in files:
        data = json.load(open(file))
        if isinstance(data, format.expected_type):
            continue
        subject = file.split(".")[0]
        singular = engine.singular_noun(subject) or subject
        if format == "object":
            new_data = objectify_list(data, singular)
        elif format == "list":
            new_data = listify_object(data, singular)
        if len(data) == len(new_data):
            json.dump(new_data, open(file, "w"), indent=2)
    print(
        f"Successfully formatted the following files to a {format}:\n"
        + "\n".join(files)
    )
