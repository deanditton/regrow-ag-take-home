import re
from sys import stdout

from models import PastureRecord


def tillage_depth(record: PastureRecord) -> bool:
    """
    Simple range check for tillage if the value exists
    """
    if record.tillage_depth:
        return 0 <= record.tillage_depth < 10
    return True


def external_id(record: PastureRecord) -> bool:
    """
    Example of possible ID using regex must be alphanumeric
    """
    simple_test = re.compile(r"[A-Za-z0-9]+")
    if record.external_account_id:
        return True if re.fullmatch(simple_test, record.external_account_id) else False
    return True


def crops_in_list(record: PastureRecord) -> bool:
    """
    Useful check type for dynamic content in this case Crops stored in DB
    """
    if record.crop_type:
        # More likely to be a list generated from a DB query to the "recognised" crop list
        crop_list = ["Corn", "Peas", "Tomatoes"]
        return record.crop_type in crop_list
    return True
