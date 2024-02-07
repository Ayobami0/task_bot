from sqlalchemy.sql import func

from sqlalchemy import (
    Enum,
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.status import Status
import config

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
    task = Column("task", String, nullable=True)
    message_link = Column("message_link", String)
    status = Column("status", Enum(Status))

    def __init__(self, task_id, task: str, message_link: str):
        self.task_id = task_id
        self.task = task
        self.status = Status.pending
        self.message_link = message_link

    def __repr__(self) -> str:
        return f"{self.task} \nStatus: {self.status}"


if config.ENVIRONMENT == "production":
    echo = False
    db_url = f"postgresql+pyscopg2://{config.PG_USER}:\
{config.PG_PASSWORD}@{config.PG_HOST}:\
{config.PG_PORT}/{config.PG_DB}"
else:
    db_url = "sqlite:///./tasks.db"
    echo = True


engine = create_engine(db_url, echo=echo)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
