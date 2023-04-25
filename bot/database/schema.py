from sqlalchemy.sql import func

from sqlalchemy import (
    CHAR,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.task import Task

Base = declarative_base()


class Tasks(Base):
    __tablename__ = "tasks"

    task_id = Column("id", Integer, primary_key=True)
    date_created = Column(
        "date_created", DateTime(timezone=True), server_default=func.now()
    )
    date_updated = Column(
        "date_updated",
        DateTime(timezone=True),
        server_onupdate=func.now(),
        server_default=func.now,
    )
    task = Column("task", String)
    status = Column("status", String)

    def __init__(self, task_id, task: Task):
        self.task_id = task_id
        self.task = task.task
        self.status = task.status

    def __repr__(self):
        return f"{self.task} \nStatus: {self.status}"


engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
