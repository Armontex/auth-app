from pydantic import BaseModel, ConfigDict


class UpdateResponse(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None

    model_config = ConfigDict(
        json_schema_extra={
            "first_name": "some-name",
            "last_name": "some-last",
            "middle_name": None,
        }
    )


class UpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "first_name": "some-new-name",
            "middle_name": "some-new-middle-name",
        }
    )
