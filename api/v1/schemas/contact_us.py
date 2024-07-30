from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ContactUsCreate(BaseModel):
    """Schema for creating a contact message."""

    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)


class ContactUsResponse(BaseModel):
    """Schema for the response of a contact message."""

    id: str
    full_name: str
    email: EmailStr
    title: str
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}


# from pydantic import BaseModel, EmailStr


# class ContactUsResponseSchema(BaseModel):
#     full_name: str
#     email: EmailStr
#     title: str  # Need review on this > to be converted to phone_number base on what I see on FE
#     message: str

#     class Config:
#         from_attributes = True


# class CreateContactUs(BaseModel):
#     """Validate the contact us form data."""

#     full_name: str
#     email: EmailStr
#     phone_number: str
#     message: str
