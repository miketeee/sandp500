from prefect import task
from sandp500financials.tasks import prefect_task_ex

def test_prefect_task():

    assert prefect_task_ex.prefect_task_ex.fn() == True