import json
from abc import ABC
from pathlib import Path
from typing import List, TYPE_CHECKING, Union, Iterable

from argilla_sdk.records._io._generic import GenericExportMixin

if TYPE_CHECKING:
    from argilla_sdk import Record


class GenericJSONIOMixin(Iterable["Record"], ABC):
    def to_json(self, path: Union[Path, str]) -> Path:
        """
        Export the records to a file on disk. This is a convenient shortcut for dataset.records(...).to_disk().

        Parameters:
            path (str): The path to the file to save the records.
            orient (str): The structure of the exported dictionary.

        Returns:
            The path to the file where the records were saved.

        """
        if isinstance(path, str):
            path = Path(path)
        if path.exists():
            raise FileExistsError(f"File {path} already exists.")
        record_dicts = [GenericExportMixin._record_to_dict(record) for record in self]
        with open(path, "w") as f:
            json.dump(record_dicts, f)
        return path

    def from_json(self, path: Union[Path, str]) -> List["Record"]:
        """Creates a DatasetRecords object from a disk path.

        Args:
            path (str): The path to the file containing the records.

        Returns:
            DatasetRecords: The DatasetRecords object created from the disk path.

        """
        with open(path, "r") as f:
            record_dicts = json.load(f)
        records = [GenericExportMixin._dict_to_record(record) for record in record_dicts]
        return records
