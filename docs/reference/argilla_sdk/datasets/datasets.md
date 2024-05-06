# `rg.Dataset`

`Dataset` is a class that represents a collection of records. It is used to store and manage records in Argilla.

## Usage Examples

### Creating a Dataset

To create a new dataset you need to define its name and settings and then publish it to the server.

```python
dataset = rg.Dataset(
    name="my_dataset",
    settings=rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.TextQuestion(name="response"),
        ],
    ),
)
dataset.publish()
```

### Retrieving an existing Dataset


To retrieve an existing dataset, use `client.datasets("my_dataset")` instead.

```python
dataset = client.datasets("my_dataset")
```

To check if a dataset exists on the server, use the `exists` method.

```python
if dataset.exists() == False:
    dataset.create()
```

To connect to an existing workspace refer to the workspace by id or object. For example:

```python
# Get an existing workspace
workspace = client.workspaces("my_workspace")
dataset = rg.Dataset(name="my_dataset", workspace=workspace)

# Use the workspace id
dataset = rg.Dataset(name="my_dataset", workspace_id="workspace_id")

# Use the first workspace
dataset = rg.Dataset(name="my_dataset")

```

---

## Class Reference

::: argilla_sdk.datasets.Dataset
    options: 
        heading_level: 3