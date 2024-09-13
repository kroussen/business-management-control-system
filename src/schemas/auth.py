from pydantic import BaseModel, EmailStr


class SignUpRequestSchema(BaseModel):
    account: EmailStr
    token: str


class SignUpResponseSchema(BaseModel):
    account: EmailStr
    message: str


class SignUpCompleteRequestSchema(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str


class SignUpCompleteResponseSchema(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str


class CheckAccountResponseSchema(BaseModel):
    message: str
    account: EmailStr


class SignInRequestSchema(BaseModel):
    account: EmailStr
    password: str


class TokenInfoSchema(BaseModel):
    access_token: str
    token_type: str
