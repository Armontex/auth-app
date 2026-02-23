from pydantic import BaseModel, ConfigDict


class ReadRolesResponse(BaseModel):
    roles: list[str]

    model_config = ConfigDict(json_schema_extra={"roles": ["user", "admin", "..."]})


class SetRoleRequest(BaseModel):
    user_id: int
    role: str

    model_config = ConfigDict(json_schema_extra={"user_id": 123, "role": "admin"})
