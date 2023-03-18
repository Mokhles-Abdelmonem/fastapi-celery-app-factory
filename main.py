from project import create_app
import uvicorn


app = create_app()
celery = app.celery_app

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
