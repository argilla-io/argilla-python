class FieldBase:
    pass


class TextField(FieldBase):
    def __init__(self, name: str, use_markdown: bool = False):
        self.name = name
        self.use_markdown = use_markdown

    def serialize(self):
        return {
            "name": self.name,
            "use_markdown": self.use_markdown,
        }
