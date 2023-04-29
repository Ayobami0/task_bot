from schema import Session, Tasks
from models.task import Task


def create(task: Task) -> None:
    with Session() as session:
        session.add(task)
        session.commit()

def read(task_id) -> Task:
    with Session() as session:
        result = session.query(Task).filter(Task.task_id == task_id).scalar()
    return result

def read_all() -> list:
    with Session() as session:
        result = session.query(Task).all()
    return result

def update(task_id, status) -> None:
    with Session() as session:
        session.query(Task).filter(Task.task_id == task_id).update({Task.status: status})
        session.commit()

def delete(task_id) -> None:
    with Session() as session:
        session.query(Task).filter(Task.task_id == task_id).delete()


task2 = Task('oludemiayobami@gmail.com\n230\n04-05-2023\n09068272767\nMTN 1GB')
task3 = Task('oludemiayobami@gmail.com\n500\n04-04-2023\n09068272767\nMTN 1GB')

create(Tasks(2, task2))
create(Tasks(3, task3))
print(read(3).date_created)
print(read(3).status)

print(read_all())