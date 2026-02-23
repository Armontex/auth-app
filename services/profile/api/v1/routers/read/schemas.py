from pydantic import BaseModel, ConfigDict


class ProfileResponse(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None
    
    model_config = ConfigDict(json_schema_extra={
        "first_name": "some-name",
        "last_name": "some-name",
        "middle_name": None
    })
