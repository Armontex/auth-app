from pydantic import BaseModel, ConfigDict


class LoginRequests(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "admin@example.com", "password": "qwerty123"}
        }
    )


class LoginResponse(BaseModel):
    access_token: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"access_token": "<token>"}}
    )
