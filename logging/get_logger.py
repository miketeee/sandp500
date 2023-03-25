from prefect import get_run_logger


def task_logger():
    logger = get_run_logger()
    return logger
