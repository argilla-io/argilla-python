from typing import Optional


class FieldBase:
    pass


class TextField(FieldBase):
    def __init__(self, name: str, use_markdown: bool = False, title: Optional[str] = None, required: bool = True):
        self.name = name
        self.use_markdown = use_markdown
        self.title = title or name
        self.required = required

    def serialize(self):
        return {
            "name": self.name,
            "use_markdown": self.use_markdown,
            "required": self.required,
        }
