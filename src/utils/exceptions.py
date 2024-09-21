from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class BadRequestException(BaseHTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class UnauthorizedException(BaseHTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class ForbiddenException(BaseHTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=403, detail=detail)
