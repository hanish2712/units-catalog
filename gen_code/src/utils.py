import json
from typing import Dict
import re


def load_json(file: str):
    """
    load json file
    """
    with open(file, "r") as fid:
        data = json.loads(fid.read())
    return data


def to_json(data: Dict, file=None):
    # Export dict to json
    if file is None:
        file = "./fileexport.json"
    with open(file, "w") as fid:
        json.dump(data, fid, indent=4, separators=(",", ":"))
    return


def string_clean(value: str):
    """
    cleans single string value
    """
    if type(value) == str:
        value = re.sub("[!#?]", "", value)  # remove punctuation
        value = re.sub(
            r"\s+", " ", value
        )  # remove any whitespace characters [\t\n\r\f\v]
        value = value.strip()  # remove front and back
        value = " ".join(value.split())  # replace multiple spaces with one
    return value


def string_charnum(value: str):
    """
    allow only character and num and single whitespace
    """
    if type(value) == str:
        value = re.sub(r"\W+", " ", value)
        value = " ".join(value.split())  # replace multiple spaces with one
    return value
