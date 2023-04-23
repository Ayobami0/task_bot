from schema import Session, Task


def create(task: Task) -> None:
    with Session() as session:
        session.add(task)
        session.commit()

def read(task_id) -> Task:
    with Session() as session:
        result = session.query(Task).filter(Task.task_id == task_id).scalar()
    return result

def update(task_id, status):
    with Session() as session:
        session.query(Task).filter(Task.task_id == task_id).update({Task.status: status})
        session.commit()
def delete(task_id):
    with Session() as session:
        session.query(Task).filter(Task.task_id == task_id).delete()


task2 = Task(2, 'oludemiayobami@gmail.com', '230', '04-05-2023', '09068272767', 'MTN 1GB', 'COMPLETED')
task3 = Task(3, 'oludemiayobami@gmail.com', '500', '04-04-2023', '09068272767', 'MTN 1GB', 'PENDING')

create(task2)
create(task3)
print(read(2))
print(read(3).status)

update(3, 'COMPLETED')
print(read(3).status)