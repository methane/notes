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


# an example mapping using the base
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str] = mapped_column(String(30))
    nickname: Mapped[Optional[str]]


class User2(Base):
    __tablename__ = "user2"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(), nullable=False)
    fullname: str = Column(String(50), nullable=False)
    nickname: str = Column(String(50), nullable=True)


def main():
    print("Hello.")
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
