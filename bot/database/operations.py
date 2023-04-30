from database.schema import Session, Tasks
from sqlalchemy import func

from models.status import Status

def create(task: str) -> None:
    with Session() as session:
        session.add(task)
        session.commit()

def read(task_id):
    with Session() as session:
        result = session.query(Tasks).filter(Tasks.task_id == task_id).scalar()
    return result

def read_by_status(status: Status):
    with Session() as session:
        count = session.query(func.count(Tasks.status)).filter(Tasks.status == status)
    return count

def read_all() -> list:
    with Session() as session:
        result = session.query(Tasks).all()
    return result

def update(task_id, status) -> None:
    with Session() as session:
        session.query(Tasks).filter(Tasks.task_id == task_id).update({Tasks.status: status})
        session.commit()

def delete(task_id) -> None:
    with Session() as session:
        session.query(Tasks).filter(Tasks.task_id == task_id).delete()
