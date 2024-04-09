from typing import Any, Dict, List, TYPE_CHECKING, Union
from collections import defaultdict

if TYPE_CHECKING:
    from argilla_sdk import Record


class GenericExportMixin:
    """This is a mixin class for DatasetRecords and Export classes.
    It handles methods for exporting records to generic python formats."""

    def _export_to_dict(
        self, records: List["Record"], flatten=True, orient="names"
    ) -> Dict[str, Union[str, float, int, list]]:
        """Export records to a dictionary with either names or record index as keys.
        Args:
            records (List[Record]): List of Record objects to export.
            flatten (bool): The structure of the exported dictionary.
                - True: The record fields, metadata, suggestions and responses will be flattened.
                - False: The record fields, metadata, suggestions and responses will be nested.
            orient (str): The orientation of the exported dictionary.
                - "names": The keys of the dictionary will be the names of the fields, metadata, suggestions and responses.
                - "index": The keys of the dictionary will be the external_id of the records.
        Returns:
            dataset_records (Dict[str, Union[str, float, int, list]]): The exported records in a dictionary format.
        """
        if orient == "names":
            dataset_records: dict = defaultdict(list)
            for record in records:
                for key, value in self.__record_to_dict(record=record, flatten=flatten).items():
                    dataset_records[key].append(value)
        elif orient == "index":
            dataset_records: dict = {}
            for record in records:
                dataset_records[record.external_id] = self.__record_to_dict(record=record, flatten=flatten)
        else:
            raise ValueError(f"Invalid value for orient parameter: {orient}")
        return dataset_records

    def _export_to_list(self, records: List["Record"], flatten=True) -> List[Dict[str, Union[str, float, int, list]]]:
        """Export records to a list of dictionaries with either names or record index as keys.
        Args:
            records (List[Record]): List of Record objects to export.
            flatten (bool): The structure of the exported dictionary.
                - True: The record fields, metadata, suggestions and responses will be flattened.
                - False: The record fields, metadata, suggestions and responses will be nested.
        Returns:
            dataset_records (List[Dict[str, Union[str, float, int, list]]]): The exported records in a list of dictionaries format.
        """
        dataset_records: list = []
        for record in records:
            dataset_records.append(self.__record_to_dict(record=record, flatten=flatten))
        return dataset_records

    def __record_to_dict(self, record: "Record", flatten=True) -> Dict[str, Any]:
        """Converts a Record object to a dictionary for export.
        Returns:
            A dictionary representing the record.
        """
        fields = record.fields.to_dict()
        metadata = record.metadata
        suggestions = record.suggestions.to_dict()
        responses = record.responses.to_dict()
        question_names = set(suggestions.keys()).union(responses.keys())
        if flatten:
            record_dict = {
                **fields,
                **metadata,
                "external_id": record.external_id,
            }
            for question_name in question_names:
                _suggestion = suggestions.get(question_name)
                if _suggestion:
                    record_dict[f"{question_name}.suggestion"] = _suggestion.pop("value")
                    record_dict.update(
                        {f"{question_name}.suggestion.{key}": value for key, value in _suggestion.items()}
                    )
                for _response in responses.get(question_name, []):
                    user_id = _response.pop("user_id")
                    record_dict[f"{question_name}.response.{user_id}"] = _response.pop("value")
                    record_dict.update(
                        {f"{question_name}.response.{user_id}.{key}": value for key, value in _response.items()}
                    )
        else:
            record_dict = {
                "fields": fields,
                "metadata": metadata,
                "suggestions": suggestions,
                "responses": responses,
                "external_id": record.external_id,
            }
        return record_dict
