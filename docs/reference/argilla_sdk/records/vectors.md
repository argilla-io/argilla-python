# `rg.Vector`

A vector is a numerical representation of a `Record` field or attribute, usually its text. They can be used to search for similar records via the UI or SDK. Vectors can be added to a record directly or as a dictionary with the key as the vector name and the value as the vector values.

## Usage Examples

Vectors can be passed to a record directly or as a dictionary with the key as the vector name and the value as the vector values:

```python
dataset.records.add(
    [
        {
            "text": "Hello World, how are you?",
            "vector_name": [0.1, 0.2, 0.3]
        }
    ]
)
```

Vectors can be passed using a mapping of the vector name to the vector values,
where the key is the vector name and the value is the vector values. The mapping \
is passed as a dictionary to the `mapping` parameter, where the key is the \
key in the data source and the value is the vector_name in the Argilla server:

```python
dataset.records.add(
    [
        {
            "text": "Hello World, how are you?",
            "x": [0.1, 0.2, 0.3]
        }
    ],
    mapping={"x": "vector_name"}
)
```

Or, vectors can be instantiated and added to a record:

```python
dataset.records.add(
    [
        rg.Record(
            fields={"text": "Hello World, how are you?"},
            vectors=[rg.Vector("embedding", [0.1, 0.2, 0.3])],
        )
    ]
)
```

::: argilla_sdk.vectors