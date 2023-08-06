from datetime import datetime
from typing import Any, List, Dict

from parsedatetime import parsedatetime


def json_converter(o: Any) -> str or None:
    """
    Simple converter for json serialization
    :param o: the object to serialize
    :return: serialized value or None
    """
    if isinstance(o, datetime):
        return o.isoformat()


def _parse_datetime_fields(items: List[Dict], fields: List[str]):
    for field in fields:
        for item in items:
            if field in item and item[field] is not None:
                cal = parsedatetime.Calendar(constants=parsedatetime.Constants(localeID="de_DE"))
                datetime_obj, _ = cal.parseDT(datetimeString=item[field])
                item[field] = datetime_obj
