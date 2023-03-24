from prefect import task

@task
def prefect_task_ex():
    return True