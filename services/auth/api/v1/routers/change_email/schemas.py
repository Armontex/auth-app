from pydantic import BaseModel, ConfigDict


class ChangeEmailRequest(BaseModel):
    email: str
    password: str
    new_email: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "user-password",
                "new_email": "new@example.com",
            }
        }
    )
