# `rg.Response`

Class for interacting with Argilla Responses of records. Responses are answers to questions by a user. Therefore, a recod question can have multiple responses, one for each user that has answered the question. A `Response` is typically created by a user in the UI or consumed from a data source as a label, unlike a `Suggestion` which is typically created by a model prediction.

## Usage Examples

Responses can be added to an instantiate `Record` directly or as a dictionary a dictionary. The following examples demonstrate how to add responses to a record object and how to access responses from a record object:

Instantiate the `Record` and related `Response` objects:

```python
dataset.records.add(
    [
        rg.Record(
            fields={"text": "Hello World, how are you?"},
            responses=[rg.Response("label", "negative", user_id=user.id)],
            external_id=str(uuid.uuid4()),
        )
    ]
)
```

Or, add a response from a dictionary where key is the question name and value is the response:

```python

dataset.records.add(
    [
        {
            "text": "Hello World, how are you?",
            "label.response": "negative",
        },
    ]
)
```

Responses can be accessed from a `Record` via their question name as an attribute:

```python

for record in dataset.records:
    for user_response in record.user_responses:
        print(record.question_name.value)

```

::: argilla_sdk.responses
