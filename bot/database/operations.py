from database.schema import Session, Tasks

from models.status import Status


def create(task: str) -> None:
    with Session() as session:
        session.add(task)
        session.commit()


def read(task_id):
    with Session() as session:
        result = session.query(Tasks).filter(Tasks.task_id == task_id).scalar()
    return result


def count_by_status(status: Status):
    with Session() as session:
        count = session.query(Tasks).filter(Tasks.status == status).count()
    return count


def read_all(limit=10, page=1) -> str:
    offset = (page - 1) * limit
    message = ""
    with Session() as session:
        for task in session.query(Tasks).order_by(Tasks.date_updated.desc()).limit(limit).offset(offset).all():
            message += f"{task.task}\nLink: {task.message_link}\nStatus: {task.status.value}\n\n"
    pagination = f"\n\nPage: {page}"
    return f'{message}{pagination}' if len(message) != 0 else 'There are no Tasks yet. Please create one'


def update(task_id, status: Status) -> None:
    with Session() as session:
        session.query(Tasks).filter(Tasks.task_id ==
                                    task_id).update({Tasks.status: status})
        session.commit()


def delete(task_id) -> None:
    with Session() as session:
        session.query(Tasks).filter(Tasks.task_id == task_id).delete()
