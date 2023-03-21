from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from . import models, schemas, utils, tasks
from project.config.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

users_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@users_router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return utils.create_user(db=db, user=user)


@users_router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = utils.get_users(db, skip=skip, limit=limit)
    return users


@users_router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = utils.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.post("/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return utils.create_user_item(db=db, item=item, user_id=user_id)


@users_router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = utils.get_items(db, skip=skip, limit=limit)
    return items


@users_router.post("/start-celery-devide-task")
def devide_task(x: int, y: int):
    task = tasks.divide.delay(x, y)
    print("task id: ", task.id)
    print("task task_id: ", task.task_id)
    return {"success":"task successfully started"}


from .controller import send_verify_code, validate_code
from .schemas import PhoneNumber, ValidateCode, Token, Message

otp_mobile_router = APIRouter(prefix="/code")

@otp_mobile_router.post("/send", response_model=Token)
def send_verify_code_handler(phone_number: PhoneNumber):
    token = send_verify_code(phone_number.phone_number)
    return Token(token=token)

@otp_mobile_router.post("/validate", response_model=Message)
def validate_code_handler(validate: ValidateCode):
    message = validate_code(validate.token, validate.code)
    return Message(message=message)