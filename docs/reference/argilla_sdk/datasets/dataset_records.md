
# rg.Dataset.records

## Usage Examples

In most cases, you will not need to create a `DatasetRecords` object directly.
Instead, you can access it via the `Dataset` object:

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
for record in dataset.records(query="question:capital", with_vectors=True):
    print(record.vectors)
```

### Adding records to a dataset

To add records to a dataset, use the `add` method. Records can be added as dictionaries or as `Record` objects. Single records can also be added as a dictionary or `Record`.

```python
# Add records to a dataset
dataset.records.add(records=[
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the capital of Germany?", "answer": "Berlin"},
])
```

When adding records from a native datasource, a mapping can be provided to map the keys in the native data structure to the fields and questions in Argilla. The dot notation is used to access suggestions and responses in the records.

```python
dataset.records.add(
    records=[{"my_label": "label.response", "my_guess": "label.suggestion", "x": "text"}],
    mapping={"my_label": "label.response", "my_guess": "label.suggestion", "x": "text"},
)
```

### Updating records in a dataset

Records can also be updated using the `id` or `external_id` to identify the records to be updated:

```python
dataset.records.update(records=[
    {"id": "1", "question": "What is the capital of France?", "answer": "Paris"},
    {"id": "2", "question": "What is the capital of Germany?", "answer": "Berlin"},
])
```

We can also use mapppings when updating records to consume data structures in its native format:

```python
dataset.records.update(
    records=[{"my_label": "label.response", "my_guess": "label.suggestion", "x": "text"}],
    mapping={"my_label": "label.response", "my_guess": "label.suggestion", "x": "text"},
)
```

### Exporting records from a dataset

Records can also be exported from `Dataset.records`. Generic python exports include `to_dict` and `to_list` methods.

```python
dataset.records.to_dict()
# {"text": ["Hello", "World"], "label": ["greeting", "greeting"]}

```

Output the records as a dictionary orientated by index:

```python
dataset.records.to_dict(orient="index")
# {"uuid": {"text": "Hello", "label": "greeting"}}
```

Output the records as a list of dictionaries:

```python
dataset.records.to_list()
# [{"text": "Hello", "label": "greeting"}, {"text": "World", "label": "greeting"}]
```

---

::: argilla_sdk.records.DatasetRecords