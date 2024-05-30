
# `rg.Dataset.records`

## Usage Examples

In most cases, you will not need to create a `DatasetRecords` object directly.
Instead, you can access it via the `Dataset` object:

!!! note "For user familiar with legacy approaches"
    1. `Dataset.records` object is used to interact with the records in a dataset. It interactively fetches records from the server in batches without using a local copy of the records. 
    2. The `log` method of `Dataset.records` is used to both add and update records in a dataset. If the record includes a known `id` field, the record will be updated. If the record does not include a known `id` field, the record will be added.
```python

### Adding records to a dataset

To add records to a dataset, use the `log` method. Records can be added as dictionaries or as `Record` objects. Single records can also be added as a dictionary or `Record`.

=== "As a `Record` object"

    You can also add records to a dataset by initializing a `Record` object directly.

    ```python	

    records = [
        rg.Record(
            fields={
                "question": "Do you need oxygen to breathe?",
                "answer": "Yes"
            },
        ),
        rg.Record(
            fields={
                "question": "What is the boiling point of water?",
                "answer": "100 degrees Celsius"
            },
        ),
    ] # (1)

    dataset.records.log(records)
    ```

    1. In a real world scenario, you might iterate over a data structure and create `Record` objects for each record. This is a more efficient way to add records to a dataset. 

=== "From a data structure"

    ```python	

    data = [
        {
            "question": "Do you need oxygen to breathe?",
            "answer": "Yes",
        },
        {
            "question": "What is the boiling point of water?",
            "answer": "100 degrees Celsius",
        },
    ] # (1)

    dataset.records.log(data)
    ```

    1. If the data structure is a list of dictionaries, the keys in the dictionary must match the fields in the dataset. In this case, the fields are `question` and `answer`. We would not advise you to to define dictionaries. Instead use the `Record` object.


=== "From a data structure with a mapping"

    ```python
    data = [
        {
            "query": "Do you need oxygen to breathe?",
            "response": "Yes",
        },
        {
            "query": "What is the boiling point of water?",
            "response": "100 degrees Celsius",
        },
    ] # (1)
    dataset.records.log(
        records=data, 
        mapping={"query": "question", "response": "answer"} # (2)
    )

    ```

    1. If the data structure is a list of dictionaries, the keys in the dictionary must match the fields in the dataset. In this case, the fields are `question` and `answer`. We would not advise you to to define dictionaries. Instead use the `Record` object.
    2. Let's say that your data structure has keys `query` and `response` instead of `question` and `answer`. You can use the `mapping` parameter to map the keys in the data structure to the fields in the dataset.

### Updating records in a dataset

Records can also be updated using the `log` method with records that contain an `id` to identify the records to be updated. As above, records can be added as dictionaries or as `Record` objects.

=== "As a `Record` object"

    You can also add records to a dataset by initializing a `Record` object directly.

    ```python	

    records = [
        rg.Record(
            metadata={"department": "toys"},
            id="2" # (1)
        ),
    ] # (1)

    dataset.records.log(records)
    ```

    1. The `id` field is required to identify the record to be updated. The `id` field must be unique for each record in the dataset. If the `id` field is not provided, the record will be added as a new record.

=== "From a data structure"

    ```python	

    data = [
        {
            "metadata": {"department": "toys"},
            "id": "2" # (1)
        },
    ] # (1)

    dataset.records.log(data)
    ```

    1. The `id` field is required to identify the record to be updated. The `id` field must be unique for each record in the dataset. If the `id` field is not provided, the record will be added as a new record.


=== "From a data structure with a mapping"

    ```python
    data = [
        {
            "metadata": {"department": "toys"},
            "my_id": "2" # (1)
        },
    ]

    dataset.records.log(
        records=data, 
        mapping={"my_id": "id"} # (2)
    )

    ```
    1. The `id` field is required to identify the record to be updated. The `id` field must be unique for each record in the dataset. If the `id` field is not provided, the record will be added as a new record.
    2. Let's say that your data structure has keys `my_id` instead of `id`. You can use the `mapping` parameter to map the keys in the data structure to the fields in the dataset.

### Iterating over records in a dataset

`Dataset.records` can be used to iterate over records in a dataset from the server. The records will be fetched in batches from the server::

```python
for record in dataset.records:
    print(record)

# Fetch records with suggestions and responses
for record in dataset.records(with_suggestions=True, with_responses=True):
    print(record.suggestions)
    print(record.responses)

# Filter records by a query and fetch records with vectors
for record in dataset.records(query="capital", with_vectors=True):
    print(record.vectors)
```

Check out the [`rg.Record`](../records/record.md) class reference for more information on the properties and methods available on a record and the [`rg.Query`](../query/query.md) class reference for more information on the query syntax.

---

## Class Reference

### `rg.Dataset.records`

::: argilla_sdk.records.DatasetRecords
    options: 
        heading_level: 3