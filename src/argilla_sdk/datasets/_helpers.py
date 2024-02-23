from typing import Any, Dict, List, Union

from argilla_sdk._models import RecordModel


def normalize_records(
    records: Union[RecordModel, Dict[str, Any], List[Union[RecordModel, Dict[str, Any]]]]
) -> List[RecordModel]:
    """Parses the records into a list of `FeedbackRecord` objects.

    Args:
        records: either a single `FeedbackRecord` or `dict` or a list of `FeedbackRecord` or `dict`.

    Returns:
        A list of `FeedbackRecord` objects.

    Raises:
        ValueError: if `records` is not a `FeedbackRecord` or `dict` or a list of `FeedbackRecord` or `dict`.
    """

    if len(records) == 0:
        raise ValueError("Expected `records` to be a non-empty list of `dict` or `FeedbackRecord`.")

    new_records = []
    for record in records:
        if isinstance(record, dict):
            new_records.append(RecordModel(**record))
        elif isinstance(record, RecordModel):
            new_records.append(record)
        else:
            raise ValueError(
                "Expected `records` to be a list of `dict` or `FeedbackRecord`," f" got type `{type(record)}` instead."
            )
    return new_records
