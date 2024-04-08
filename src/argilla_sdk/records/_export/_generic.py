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
        dataset_records: dict = {}
        if orient == "names":
            dataset_records.update(self.__dict_orient_names(records, flatten))
        elif orient == "index":
            dataset_records.update(self.__dict_orient_index(records, flatten))
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
            if flatten:
                dataset_records.append(self.__flatten_record(record))
            else:
                dataset_records.append(self.__nest_record(record))
        return dataset_records

    #########################
    # Dict Oriented Exports
    #########################

    def __dict_orient_names(self, records: List["Record"], flatten: bool = True) -> Dict[str, Any]:
        """Orient a record with field, question, metadata, suggestion and response names as keys."""
        dataset_records: defaultdict = defaultdict(list)
        for record in records:
            if flatten:
                record_dict = self.__flatten_record(record)
            else:
                record_dict = self.__nest_record(record)
            for key, value in record_dict.items():
                dataset_records[key].append(value)
        return dataset_records

    def __dict_orient_index(self, records: List["Record"], flatten: bool = True) -> Dict[str, Any]:
        """Orient a record with external_id as keys."""
        dataset_records: dict = {}
        for record in records:
            if flatten:
                dataset_records[record.external_id] = self.__flatten_record(record)
            else:
                dataset_records[record.external_id] = self.__nest_record(record)
        return dataset_records

    #########################
    # Flattening Records
    #########################

    def __flatten_record(self, record: "Record") -> Dict[str, Any]:
        """Flatten a record with field, question, metadata, suggestion and response names as keys."""
        record_dict = {}
        record_dict["external_id"] = record.external_id
        record_dict.update(record.fields.to_dict())
        record_dict.update(self.__flatten_record_metadata(record))
        record_dict.update(self.__flatten_record_suggestions(record))
        record_dict.update(self.__flatten_record_responses(record))
        return record_dict

    def __flatten_record_suggestions(self, record: "Record") -> Dict[str, Any]:
        """Flatten the suggestions of a record."""
        record_suggestion_dict = {}
        for suggestion in record.suggestions:
            record_suggestion_dict[f"{suggestion.question_name}.suggestion"] = suggestion.value
            record_suggestion_dict[f"{suggestion.question_name}.score"] = suggestion.score
            if suggestion.agent is not None:
                record_suggestion_dict[f"{suggestion.question_name}.agent"] = suggestion.agent
        return record_suggestion_dict

    def __flatten_record_responses(self, record: "Record") -> Dict[str, Any]:
        """Flatten the responses of a record."""
        record_response_dict = {}
        for response in record.responses:
            record_response_dict[response.question_name] = response.value
            record_response_dict[f"{response.question_name}.user_id"] = response.user_id
            record_response_dict[f"{response.question_name}.status"] = response.status
        return record_response_dict

    def __flatten_record_metadata(self, record: "Record") -> Dict[str, Any]:
        """Flatten the metadata of a record."""
        record_metadata_dict = {}
        for key, value in record.metadata.items():
            record_metadata_dict[key] = value
        return record_metadata_dict

    #########################
    # Nesting Records
    #########################

    def __nest_record(self, record: "Record") -> Dict[str, Any]:
        """Nest a record with field, question, metadata, suggestion and response names as keys."""
        record_dict = {}
        record_dict["external_id"] = record.external_id
        record_dict["fields"] = record.fields
        record_dict["metadata"] = record.metadata
        record_dict["responses"] = self.__nested_record_responses(record)
        record_dict["suggestions"] = self.__nested_record_suggestions(record)
        return record_dict

    def __nested_record_responses(self, record: "Record") -> Dict[str, Any]:
        """Nest the responses of a record."""
        record_response_dict = {}
        for response in record.responses:
            record_response_dict[response.question_name] = {
                "value": response.value,
                "user_id": response.user_id,
                "status": response.status,
            }
        return record_response_dict

    def __nested_record_suggestions(self, record: "Record") -> Dict[str, Any]:
        """Nest the suggestions of a record."""
        record_suggestion_dict = {}
        for suggestion in record.suggestions:
            record_suggestion_dict[suggestion.question_name] = {
                "value": suggestion.value,
                "score": suggestion.score,
                "agent": suggestion.agent,
            }
        return record_suggestion_dict
