from pydantic import BaseModel, ConfigDict


class RegisterRequests(BaseModel):
    email: str
    first_name: str
    middle_name: str | None = None
    last_name: str
    password: str
    confirm_password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "some-first-name",
                "middle_name": "some-middle-name",
                "last_name": "some-last-name",
                "email": "admin@example.com",
                "password": "some-password",
                "confirm_password": "some-password",
            }
        }
    )


class RegisterResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"id": 1, "email": "admin@example.com"}}
    )
