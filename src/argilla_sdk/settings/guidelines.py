from pydantic import BaseModel, validator


class Guidelines(BaseModel):
    guidelines: str

    @validator("guidelines")
    def __process_guidelines(cls, guidelines):
        # TODO: Add validation, error handling, and processing for guidelines.
        return guidelines

    def __str__(self) -> str:
        return str(self.guidelines)

    def serialize(self):
        return {
            "guidelines_str": self.guidelines,
        }
