from pydantic import BaseModel, ConfigDict


class ValidationErrorResponse(BaseModel):
    errors: list[dict]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "field1": ["error message 1", "error message 2"],
                        "field2": ["error message 1"],
                    }
                ]
            }
        }
    )


class TokenVerifyErrorResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"detail": "Invalid or expired token."}
        }
    )
    
class LoginErrorResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"detail": "Invalid credentials."}
        }
    )
    
    
class UserNotExistsResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"detail": "This user does not exist"}
        }
    )