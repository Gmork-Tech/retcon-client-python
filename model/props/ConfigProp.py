import string
from dataclasses import dataclass, field

import isodate


def from_json(prop: dict):
    my_prop = ConfigProp(**prop)
    if prop["kind"] is "STRING":
        my_prop.value = str(prop["value"])
    elif prop["kind"] is "NUMBER":
        my_prop.value = float(prop["value"])
    elif prop["kind"] is "BOOLEAN":
        my_prop.value = bool(prop["value"])
    elif prop["kind"] is "TIMESTAMP":
        my_prop.value = isodate.parse_datetime(prop["value"])
    elif prop["kind"] is "DURATION":
        my_prop.value = isodate.parse_duration(prop["value"])
    elif prop["kind"] is "OBJECT":
        return my_prop
    elif prop["kind"] is "ARRAY":
        my_prop.value = list(prop["value"])
    else:
        print("Unknown property kind:" + str(prop["kind"]))
    return my_prop


@dataclass
class ConfigProp:
    id: int = field()
    priority: int = field()
    kind: string = field()
    nullable: bool = field()
    val: any = field()

    def __lt__(self, other):
        return self.priority < other.priority
