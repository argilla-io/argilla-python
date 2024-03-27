import warnings
from typing import Any, Dict
from uuid import uuid4

from argilla_sdk._models import RecordModel, SuggestionModel
from argilla_sdk.settings import FieldType, QuestionType


def dict_to_record_model(data: dict, schema: Dict[str, Any]) -> RecordModel:
    """Converts a Record object to a record dictionary."""

    fields = {}
    suggestions = []

    for attribute, value in data.items():
        if attribute not in schema:
            warnings.warn(f"Record attribute {attribute} is not in the schema. Skipping.")
            continue

        schema_item = schema.get(attribute)
        if isinstance(schema_item, FieldType):
            fields[attribute] = value
        elif isinstance(schema_item, QuestionType):
            suggestion = SuggestionModel(value=value, question_id=schema_item.id, question_name=attribute)
            suggestions.append(suggestion.model_dump())
        else:
            warnings.warn(f"Property {attribute} is not a valid schema item. Skipping.")

    return RecordModel(
        id=data.get("id") or str(uuid4()),
        fields=fields,
        suggestions=suggestions,
        external_id=data.get("external_id"),
    )
