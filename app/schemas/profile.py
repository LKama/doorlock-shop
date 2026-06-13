from pydantic import BaseModel


class UpdateProfileRequest(BaseModel):
    name: str
    email: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str