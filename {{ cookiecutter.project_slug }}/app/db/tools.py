from typing import Any, Sequence

from databases.backends.postgres import Record


def parse_records(records: Sequence[Record]) -> Sequence[dict[str, Any]]:
    return [to_dict(record) for record in records]


def to_dict(record: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in record:
        set_value(result, key, record[key])
    return result


def set_value(d: dict[str, Any], key: str, val: Any) -> None:  # noqa: ANN401
    key_parts = key.split("__", 1)
    if len(key_parts) == 1:
        d[key] = val
    else:
        key, remainder = key_parts
        if key not in d:
            d[key] = {}
        set_value(d[key], remainder, val)
