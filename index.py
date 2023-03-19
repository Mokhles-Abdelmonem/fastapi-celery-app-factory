from project import create_app
import uvicorn
from tasks2 import celery_app , celery_router


app = create_app()
celery = celery_app
app.include_router(celery_router)

if __name__ == '__main__':
    uvicorn.run('index:app', reload=True)
