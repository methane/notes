header = """\
from typing import Optional

from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine =create_engine("sqlite:///:memory:", future=True)


# declarative base class
class Base(DeclarativeBase):
    pass

"""

template = """\
class User{0}(Base):
    __tablename__ = "user{0}"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str] = mapped_column(String(30))
    nickname: Mapped[Optional[str]]

"""

template2 = """\
class User{0}(Base):
    __tablename__ = "user{0}"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(), nullable=False)
    fullname: str = Column(String(50), nullable=False)
    nickname: str = Column(String(50), nullable=True)

"""

N=10000

with open("model_typed.py", "w") as f:
    f.write(header)
    for i in range(1, N+1):
        f.write(template.format(i))


with open("model_legacy.py", "w") as f:
    f.write(header)
    for i in range(1, N+1):
        f.write(template2.format(i))
