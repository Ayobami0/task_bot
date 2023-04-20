from models.task import Task


class Tasks:
    _tasks = {}

    @classmethod
    def count(cls):
        cls._tasks.count()

    @classmethod
    def add(cls, task: Task, id_: str):
        cls._tasks[id_] = task

    @classmethod
    def remove(cls, id_):
        cls._tasks.pop(id_)

    @classmethod
    def update(cls, id_, updated_task):
        try:
            cls._tasks[id_] = updated_task
        except KeyError():
            print('Key not in map')

    @classmethod
    def get(cls, id_):
        return cls._tasks.get(id_)

    @classmethod
    def get_all(cls):
        string = ''
        if len(cls._tasks) == 0:
            return 'There are no tasks'
        for t in cls._tasks.values():
            string += f"""
{t.customer_email_address}
{t.service_amount}
{t.service_number}
{t.service_type}
{t.service_date}
{t.status}\n"""
        string.rstrip()
        return string;

    @classmethod
    def get_pendings(cls):
        count = 0
        for t in cls._tasks.values():
            if t.status == 'PENDING':
                count += 1
        return count

    @classmethod
    def get_processing(cls):
        count = 0
        for t in cls._tasks.values():
            if t.status == 'PROCESSING':
                count += 1
        return count

    @classmethod
    def get_resolved(cls):
        count = 0
        for t in cls._tasks.values():
            if t.status == 'RESOLVED':
                count += 1
        return count

    @classmethod
    def get_canceled(cls):
        count = 0
        for t in cls._tasks.values():
            if t.status == 'CANCELED':
                count += 1
        return count
    
    @classmethod
    def get_closed(cls):
        count = 0
        for t in cls._tasks.values():
            if t.status == 'CLOSED':
                count += 1
        return count
