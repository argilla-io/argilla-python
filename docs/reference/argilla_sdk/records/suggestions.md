# `rg.Suggestion`

Class for interacting with Argilla Suggestions of records. Suggestions are typically created by a model prediction, unlike a `Response` which is typically created by a user in the UI or consumed from a data source as a label.

## Usage Examples

### Adding records with suggestions

Suggestions can be added to a record directly or via a dictionary structure. The following examples demonstrate how to add suggestions to a record object and how to access suggestions from a record object:

Add a response from a dictionary where key is the question name and value is the response:

```python
dataset.records.add(
    [
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "label.suggestion.response": "negative",
            "label.suggestion.score": 0.9,
        },
    ]
)
```
Or, instantiate the `Record` and related `Suggestions` objects directly, like this:

```python
dataset.records.add(
    [
        rg.Record(
            fields={"text": "Hello World, how are you?"},
            suggestions=[rg.Suggestion("negative", "label", score=0.9, agent="model_name")],
        )
    ]
)
```

### Iterating over records with suggestions

Just like responses, suggestions can be accessed from a `Record` via their question name as an attribute of the record. So if a question is named `label`, the suggestion can be accessed as `record.label`. The following example demonstrates how to access suggestions from a record object:

```python
for record in dataset.records(with_suggestions=True):
    print(record.suggestions.label)
```

---

## Class Reference

### `rg.Suggestion`

::: argilla_sdk.suggestions.Suggestion
    options: 
        heading_level: 3