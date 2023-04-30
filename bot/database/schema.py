from sqlalchemy.sql import func

from sqlalchemy import (
    Enum,
    Column,
    DateTime,
    Integer,
    String,
    create_engine,)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.status import Status

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
        server_default=func.now(),
    )
    task = Column("task", String)
    status = Column("status", Enum(Status))

    def __init__(self, task_id, task: str):
        self.task_id = task_id
        self.task = task
        self.status = Status.pending

    def __repr__(self) -> str:
        return f"{self.task} \nStatus: {self.status}"


engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
