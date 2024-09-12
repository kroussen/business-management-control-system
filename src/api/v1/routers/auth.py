from fastapi import APIRouter

router = APIRouter(prefix='/auth')


@router.get("/check_account/{account}")
async def check_account():
    return 200


@router.post("/sign-up")
async def sign_up():
    return 200


@router.post("/sign-up-complete")
async def sign_up_complete():
    return 200


@router.post("/sign-in")
async def sign_in():
    return 200
