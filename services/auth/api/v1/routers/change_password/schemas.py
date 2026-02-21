from pydantic import BaseModel, ConfigDict


class ChangePasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "old_password": "old-password",
                "new_password": "new-password",
            }
        }
    )
