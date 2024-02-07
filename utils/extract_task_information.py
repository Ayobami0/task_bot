def extract_task(task: str) -> dict:
    ext_task = task.splitlines()

    task_dict = {
        "email_address": ext_task[0],
        "service_amount": ext_task[1],
        "service_number": ext_task[2],
        "service_type": ext_task[3],
        "service_date": ext_task[4],
        "task_status": 'PENDING'
    }

    return task_dict
