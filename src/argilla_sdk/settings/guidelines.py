class GuidelinesBase:
    pass


class Guidelines:
    def __init__(self, guidelines: str):
        self.guidelines = guidelines

    def serialize(self):
        return {
            "guidelines_str": self.guidelines,
        }

    def __str__(self) -> str:
        return str(self.guidelines)