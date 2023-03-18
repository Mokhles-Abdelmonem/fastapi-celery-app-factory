from project.celery_worker.celery_utils import celery_app 


app = celery_app()

@app.task(bind=True)
def divide(self, x, y):
    import time
    time.sleep(5)
    task_id = self.request.id
    print("task_id >>>>>>>>>>>>", task_id)
    return task_id