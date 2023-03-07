import re
from typing import Union


def normalize_name(name):
    res = re.sub(r'\W+', '', name)
    return res


def get_cname_company():
    return "com1"


def get_cname_resolution():
    return "res1"


def get_cname_meeting():
    return "meet1"


def get_cname_deed():
    return "deed1"


def get_cname_voting():
    return "vot1"


def get_cname_application():
    return "app1"


def get_cname_assurance():
    return "ass1"


def get_cname_shareholder(shareholder: Union[dict, str]):
    if isinstance(shareholder, str):
        name = shareholder
    else:
        name = shareholder['name']

    return "sh_" + normalize_name(name)


def get_cname_director(director: Union[str, dict]):
    if isinstance(director, str):
        name = director
    else:
        name = director['name']

    return "dir_" + normalize_name(name)


def get_cname_person(person: dict):
    name = person['name']
    return "pers_" + normalize_name(name)
