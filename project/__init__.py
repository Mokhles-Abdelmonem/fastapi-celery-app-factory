from fastapi import FastAPI
from project.celery_worker.celery_utils import celery_app 

def create_app() -> FastAPI:
    app = FastAPI()
    # app.celery_app = celery_app() 

    from project.users.router import users_router, otp_mobile_router
    app.include_router(users_router)
    app.include_router(otp_mobile_router)

    @app.get("/hello_world")
    async def root():
        return {"message": "Hello World"}

    return app
