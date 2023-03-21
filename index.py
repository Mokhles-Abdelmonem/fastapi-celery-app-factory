from project import create_app
import uvicorn
from tasks2 import celery_app , celery_router


from dotenv import load_dotenv
import sendlk
import os

# Load the .env file
load_dotenv(".env")

SENDLK_TOKEN = os.environ.get("SENDLK_TOKEN", "sendlk-token")
SECRET = os.environ.get("SECRET", "my-super-secret")

sendlk.initialize(SENDLK_TOKEN, SECRET)

app = create_app()
celery = celery_app
app.include_router(celery_router)

if __name__ == '__main__':
    uvicorn.run('index:app', reload=True)
