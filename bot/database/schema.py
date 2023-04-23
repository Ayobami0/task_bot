from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column("id", Integer, primary_key=True)
    amount = Column("amount", Integer)
    date = Column("date", String)
    biller_number = Column("biller_number", String)
    biller = Column("biller", String)
    email = Column("email", String)
    status = Column("status", String)

    def __init__(
        self, 
        task_id,
        email, 
        amount, 
        date, 
        biller_number, 
        biller,
        status,
        ):
        self.task_id = task_id
        self.amount = amount
        self.date = date
        self.biller_number = biller_number
        self.biller = biller
        self.email = email
        self.status = status

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

# task1 = Task(1, 'oludemiayobami@gmail.com', '200', '04-03-2023', '09068272767', 'MTN 1GB', 'PENDING')
# task2 = Task(2, 'oludemiayobami@gmail.com', '230', '04-05-2023', '09068272767', 'MTN 1GB', 'COMPLETED')
# task3 = Task(3, 'oludemiayobami@gmail.com', '500', '04-04-2023', '09068272767', 'MTN 1GB', 'PENDING')

# session.add(task1)
# session.add(task2)
# session.add(task3)

# session.commit()

# results = session.query(Task).all()
# print(results)