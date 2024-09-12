import uvicorn

from fastapi import FastAPI

from api import router


def create_fast_api_app() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.include_router(router, prefix='/api')
    return fastapi_app


app = create_fast_api_app()

if __name__ == "__main__":
    uvicorn.run(app='main:app', port=8000, reload=True)
