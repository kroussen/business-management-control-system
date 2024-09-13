from fastapi import APIRouter, Depends
from pydantic import EmailStr

from schemas.auth import (
    SignUpRequestSchema,
    SignUpResponseSchema,
    SignUpCompleteRequestSchema,
    SignUpCompleteResponseSchema,
    CheckAccountResponseSchema,
    SignInRequestSchema,
    TokenInfoSchema
)
from api.v1.services.auth import AuthService

router = APIRouter(prefix='/auth')


@router.get("/check_account/{account}", response_model=CheckAccountResponseSchema)
async def check_account(account: EmailStr, service: AuthService = Depends()) -> CheckAccountResponseSchema:
    return await service.check_account(account=account)


@router.post("/sign-up", response_model=SignUpResponseSchema)
async def sign_up(schema: SignUpRequestSchema, service: AuthService = Depends()) -> SignUpResponseSchema:
    return await service.sign_up(schema=schema)


@router.post("/sign-up-complete", response_model=SignUpCompleteResponseSchema)
async def sign_up_complete(schema: SignUpCompleteRequestSchema,
                           service: AuthService = Depends()) -> SignUpCompleteResponseSchema:
    return await service.sign_up_complete(schema=schema)


@router.post("/sign-in")
async def sign_in(schema: SignInRequestSchema, service: AuthService = Depends()) -> TokenInfoSchema:
    return await service.sign_in(schema=schema)
