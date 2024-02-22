from dataclasses import dataclass

from typing import Optional


@dataclass
class TextField:
    name: str
    use_markdown: bool = False
    title: Optional[str] = None
    required: bool = True

    def __post_init__(self):
        self.title = self.title or self.name
        self.name = self.name.lower().replace(" ", "_")

    def serialize(self):
        return {
            "name": self.name,
            "use_markdown": self.use_markdown,
            "required": self.required,
        }
