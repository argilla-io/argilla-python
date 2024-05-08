
# `rg.Dataset.records`

## Usage Examples

In most cases, you will not need to create a `DatasetRecords` object directly.
Instead, you can access it via the `Dataset` object:

### Adding records to a dataset

To add records to a dataset, use the `add` method. Records can be added as dictionaries or as `Record` objects. Single records can also be added as a dictionary or `Record`.

```python
import argilla_sdk as rg

# Create a dataset
dataset = rg.Dataset(
    name="my_dataset",
    settings=rg.Settings(
        fields=[
            rg.TextField(name="question"),
        ],
        questions=[
            rg.TextQuestion(name="answer"),
        ],
    ),
)

# Publish the dataset to the server
dataset.publish()

# Add records to a dataset
dataset.records.add(
    records=[
    {
        "question": "What is the capital of France?",  # 'question' matches the `rg.TextField` name
        "answer": "Paris" # 'answer' matches the `rg.TextQuestion` name
    },
    {
        "question": "What is the capital of Germany?", 
        "answer": "Berlin"
    },
])
```

When adding records from a native datasource, a mapping can be provided to map the keys in the native data structure to the fields and questions in Argilla. The dot notation is used to access suggestions and responses in the records.

```python
dataset.records.add(
    records=[
        {"input": "What is the capital of France?", "output": "Paris"},
        {"input": "What is the capital of Germany?", "output": "Berlin"},
    ],
    mapping={"input": "question", "output": "answer"}, # Maps 'input' to 'question' and 'output' to 'answer'
)
```

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

### Updating records in a dataset

Records can also be updated using the `id` or `external_id` to identify the records to be updated:

```python
# Add records to a dataset
dataset.records.add(
    records=[
        {
            "id": "1",
            "question": "What is the capital of France?",
            "answer": "F",
        },
        {
            "id": "2",
            "question": "What is the capital of Germany?",
            "answer": "Berlin"
        },
    ]
)

# Update records in a dataset
dataset.records.update(
    records=[
        {
            "id": "1",  # matches id used in `Dataset.records.add`
            "question": "What is the capital of France?",
            "answer": "Paris",
        }
    ]
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

## Class Reference

::: argilla_sdk.records.DatasetRecords
    options: 
        heading_level: 3