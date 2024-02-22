from dataclasses import dataclass


@dataclass
class Guidelines:
    guidelines: str

    def __post_init__(self):
        self.guidelines = self.__process_guidelines(guidelines=self.guidelines)

    def __str__(self) -> str:
        return str(self.guidelines)

    def __process_guidelines(self, guidelines):
        # TODO: Add validation, error handling, and processing for guidelines.
        return guidelines

    def serialize(self):
        return {
            "guidelines_str": self.guidelines,
        }
