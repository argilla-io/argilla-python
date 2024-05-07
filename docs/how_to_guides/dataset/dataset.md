---
description: In this section, we will provide a step-by-step guide to show how to manage datasets.
---

# Dataset management

This guide provides an overview of datasets, explaining the basics of how to set them up and manage them in Argilla.

## Dataset

A **dataset** is a collection of records that you can configure for labelers to provide feedback using the UI. Depending on the specific requirements of your task, you may need various types of feedback. You can customize the dataset to include different kinds of questions, so the first step will be to define the aim of your project and the kind of data and feedback you will need. With this information, you can start configuring a dataset by defining fields, questions, metadata, vectors, and guidelines through settings.

### Dataset model

A dataset is defined in the `Dataset` class that has the following arguments:

* `id`: The unique identifier of the dataset.
* `name`: The name of the dataset. It has to be unique.
* `workspace` (optional): The workspace object or its name where the dataset will be stored. Defaults to the first workspace.
* `settings`: The settings of the dataset to customize it for your task. They include the guidelines, fields, questions, metadata and vectors.
* `status` (optional): The status of the dataset. It can be `draft` or `ready`. Defaults to `ready`.
* `client`: The client used to interact with Argilla.

> Check the [Dataset - Python Reference](../../reference/argilla_sdk/datasets/dataset.md) to see the attributes, arguments, and methods of the `Dataset` class in detail.

```python
rg.Dataset(
    name="name",
    workspace=workspace,
    settings=settings,
    status="ready",
    client=client,
)
```

### Who can manage datasets

Only users with the `owner` role can manage (create, retrieve, update and delete) all the datasets.

The users with the `admin` role can manage (create, retrieve, update and delete) the datasets in the workspaces they have access to.

## How-to guide

This section starts by showing how to create a basic dataset in Argilla, and then how to list all the datasets available in each workspace and retrieve a specific one. Finally, the guide covers the steps to update and delete a dataset.

### Create a dataset

To create a dataset, you can define it in the `Dataset` class and then call the `publish` method that will send the dataset to the server so that it can be visualized in the UI. If the dataset does not appear in the UI, you may need to click the refresh button to update the view.

> For further customization of the dataset settings (fields, questions, metadata, vectors and guidelines), check this [how-to guide](settings.md). 

> The created dataset will be empty, to add the records refer to this [how-to guide](../record/index.md).

```python
import argilla_sdk as rg

client = rg.Argilla(api_url="<api_url>", api_key="<api_key>")

settings = rg.Settings(
    guidelines="These are some guidelines.",
    fields=[
        rg.TextField(
            name="text",
        ),
    ],
    questions=[
        rg.LabelQuestion(name="label", labels=["label_1", "label_2", "label_3"]),
    ],
)

dataset = rg.Dataset(
    name="my_dataset",
    workspace="my_workspace",
    settings=settings,
    client=client,
)

dataset.publish()
```
!!! tip "Accessing attributes"
    Access the attributes of a dataset by calling them directly on the `dataset` object. For example, `dataset.id`, `dataset.name` or `dataset.settings`. You can similarly access the fields, questions, metadata, vectors and guidelines. For instance, `dataset.fields` or `dataset.questions`.

### List datasets

You can list all the datasets available in a workspace using the `datasets` attribute of the `Workspace` class. You can also use `len(workspace.datasets)` to get the number of datasets in a workspace.

```python
import argilla_sdk as rg

client = rg.Argilla(api_url="<api_url>", api_key="<api_key>")

workspace = client.workspaces("my_workspace")

datasets = workspace.datasets

for dataset in datasets:
    print(dataset)
```

### Retrieve a dataset

You can retrieve a dataset by calling the `datasets` method on the `Argilla` class and passing the name of the dataset as an argument. By default, this method attempts to retrieve the dataset from the first workspace. If the dataset is in a different workspace, you must specify either the workspace name or id as an argument.

```python
import argilla_sdk as rg

client = rg.Argilla(api_url="<api_url>", api_key="<api_key>")

workspace = client.workspaces("my_workspace")

# Retrieve the dataset from the first workspace
retrieved_dataset = client.datasets(name="my_dataset")

# Retrieve the dataset from the specified workspace
retrieved_dataset = client.datasets(name="my_dataset", workspace=workspace)

```

### Check dataset existence

You can check if a dataset exists by calling the `exists` method on the `Dataset` class. This method returns a boolean value.

```python
import argilla_sdk as rg

client = rg.Argilla(api_url="<api_url>", api_key="<api_key>")

dataset = client.datasets(name="my_dataset")

dataset_existed = dataset.exists()
dataset_existed
```

### Update a dataset

You can update a dataset by calling the `update` method on the `Dataset` class and passing the new settings as an argument.

> For further information on how to update the dataset settings (fields, questions, metadata, vectors and guidelines), check this [how-to guide](settings.md).

!!! note
    Keep in mind that once your dataset is published, only the guidelines can be updated.

```python
import argilla_sdk as rg

client = rg.Argilla(api_url="<api_url>", api_key="<api_key>")

dataset_to_update = client.datasets(name="my_dataset")

settings_to_update = rg.Settings(
    guidelines="These are some updated guidelines.",
    fields=[
        rg.TextField(
            name="text",
        ),
    ],
    questions=[
        rg.LabelQuestion(name="label", labels=["label_4", "label_5", "label_6"]),
    ],
)

dataset_to_update.settings = settings_to_update

dataset_updated = dataset_to_update.update()
dataset_updated
```

### Delete a dataset

You can delete an existing dataset by calling the `delete` method on the `Dataset` class.

```python
import argilla_sdk as rg

client = rg.Argilla(api_url="<api_url>", api_key="<api_key>")

dataset_to_delete = client.datasets(name="my_dataset")

dataset_deleted = dataset_to_delete.delete()
```