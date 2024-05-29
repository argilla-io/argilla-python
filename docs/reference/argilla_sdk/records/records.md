# `rg.Record`

The `Record` object is used to represent a single record in Argilla. It contains fields, suggestions, responses, metadata, and vectors.

## Usage Examples

### Creating a Record

To create records, you can use the `Record` class. The `Record` class requires a `fields` parameter, which is a dictionary of field names and values. The field names must match the field names in the dataset's `Settings` object to be accepted.

```python
records = [
        rg.Record(
            fields={"text": "Hello World, how are you?"},
        ),
    ]
```

### Accessing Record Attributes

The `Record` object has suggestions, responses, metadata, and vectors attributes that can be accessed directly whilst iterating over records in a dataset.

```python
for record in dataset.records(
    with_suggestions=True, 
    with_responses=True, 
    with_metadata=True, 
    with_vectors=True
    ):
    print(record.suggestions)
    print(record.responses)
    print(record.metadata)
    print(record.vectors)
```

Record properties can also be updated whilst iterating over records in a dataset.

```python
for record in dataset.records(with_metadata=True):
    record.metadata = {"department": "toys"}
```

For changes to take effect, the user must call the `update` method on the `Dataset` object.


---

## Class Reference

### `rg.Record`

::: argilla_sdk.records.Record
    options: 
        heading_level: 3