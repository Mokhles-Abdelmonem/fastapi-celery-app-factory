from celery import Celery , shared_task
from celery.schedules import crontab
import schedule
import time

celery_app = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)


# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

@celery_app.task(bind=True)
def test(self, arg):
    task_id = self.request.id
    print("task_id from test >>>>>>>>>>>>", task_id)
    print(arg)


@celery_app.task
def add(x, y):
    z = x + y
    print(z)
    return("add resuts >>>>>>>>>>>>>",z)





def add_contib(x, y):
    res = add.delay(x, y)
    return("add resuts >>>>>>>>>>>>>",res)




@celery_app.task
def add_periodic(x, y):
    schedule.every(1).seconds.do(add_contib, x, y)
    while True:
        schedule.run_pending()
        time.sleep(3)


from fastapi import APIRouter
celery_router = APIRouter(
    prefix="/celery",
    tags=["celery"]
)

@celery_router.post("/start-periodic-add-task")
def add_task(x: int, y: int):
    add_periodic.delay(x, y)
    return {"success": "task has been added"}