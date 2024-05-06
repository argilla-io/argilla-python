# Fields

Fields in Argilla are define the content of a record that will be reviewed by a user. Fields can be either text or vector form.

## Usage Examples

To define a field, instantiate the `TextField` class and pass it to the `fields` parameter of the `Settings` class.

```python
text_field = rg.TextField(name="text")
markdown_field = rg.TextField(name="text", use_markdown=True)
```

To define a vector field, instantiate the `VectorField` class and pass it to the `fields` parameter of the `Settings` class.

```python
vector_field = rg.VectorField(name="embedding")
```

The `fields` parameter of the `Settings` class can accept a list of fields, like this:

```python
settings = rg.Settings(
    fields=[
        rg.TextField(name="text"),
    ],
    vectors=[
        rg.VectorField(name="embedding"),
    ],
)
```

---

## Class References

::: argilla_sdk.settings.TextField
    options: 
        heading_level: 3

::: argilla_sdk.settings.VectorField
    options: 
        heading_level: 3