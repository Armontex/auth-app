from pydantic import BaseModel, ConfigDict


class ReadPermissionsResponse(BaseModel):
    permissions: list[str]

    model_config = ConfigDict(json_schema_extra={"permissions": ["profile:me:read", "role:read", "..."]})

