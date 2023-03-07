import re
from typing import Union


def normalize_name(name):
    res = re.sub(r'\W+', '', name)
    return res


def get_cname_company():
    return "com1"


def get_cname_ci_resolution():
    return "ci_res1"


def get_cname_per_resolution():
    return "per_res1"


def get_cname_ci_meeting():
    return "ci_meet1"


def get_cname_per_meeting():
    return "per_meet1"


def get_cname_ci_voting():
    return "ci_vot1"


def get_cname_per_voting():
    return "per_vot1"


def get_cname_subscriberlist():
    return "subl1"


def get_cname_subscription(subscription):
    return "sub_" + subscription['name']


def get_cname_declaration(declaration):
    return "dcl_" + declaration['signer']


def get_cname_application():
    return "app1"


def get_cname_assurance():
    return "ass1"


def get_cname_amendedAoA():
    return "aoa1"


def get_cname_shareholder(shareholder: Union[str, dict]):
    if isinstance(shareholder, str):
        name = shareholder
    elif 'name' in shareholder:
        name = shareholder['name']
    else:
        name = shareholder['signer']

    return "sh_" + normalize_name(name)


def get_cname_director(director: Union[str, dict]):
    if isinstance(director, str):
        name = director
    else:
        name = director['name']

    return "dir_" + normalize_name(name)


def get_cname_person(person: dict):
    if isinstance(person, str):
        name = person
    else:
        name = person['name']

    return "pers_" + normalize_name(name)
