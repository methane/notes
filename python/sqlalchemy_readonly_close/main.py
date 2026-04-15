from typing import Any

from flask import Flask
from sqlalchemy import create_engine, Column, Integer, engine as sa_engine
from sqlalchemy import event
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy.exc import DisconnectionError


engine = create_engine(
    "mysql://root@127.0.0.1:3306/test", echo="debug", echo_pool="debug", pool_pre_ping=True
)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


@event.listens_for(engine, "checkout")
def handle_pool_checkout(
    dbapi_connection: Any, connection_record: Any, connection_proxy: Any
) -> None:
    """
    コネクションプールからコネクションをチェックアウトした時に innodb_read_only をチェックし、
    failover後のread replicaになっていないかをチェックする。

    https://docs.sqlalchemy.org/en/21/core/events.html#sqlalchemy.events.PoolEvents.checkout
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("SELECT @@innodb_read_only")
    read_only = cursor.fetchone()[0]
    if read_only:
        raise DisconnectionError("detected innodb_read_only=1")


@event.listens_for(engine, "handle_error")
def handle_readonly_error(context: sa_engine.ExceptionContext) -> None:
    """
    read_only / innodb_read_only 時に発生するエラーで接続を invalidate する

    Auroraのfailover時にread_onlyモードになりエラーが発生するので、その接続を再利用しないようにすることで
    failover 後に primary に接続させる。
    """
    orig = context.original_exception
    if not isinstance(orig, Exception):
        return

    # MySQL Driverの例外は .args[0] がエラーコードになっている。
    if args := getattr(orig, "args", None):
        # read replica で発生するエラー.
        # 1015: Can't lock file (errno: 165 - Table is read only)
        # 1290: The MySQL server is running with the --read-only option so it cannot execute this statement
        # 1836: Running in read-only mode
        if args[0] in (1015, 1290, 1836) and context.connection is not None:
            # connection.invalidate(exception=orig) を使うとconnectionがすぐにcloseされてしまい
            # このあとの cursor.close() でエラーが発生してログを汚してしまう。
            # このコネクションがpoolに戻されないようにdetachだけを行う。
            context.connection.detach()


app = Flask(__name__)


class Counter(Base):
    __tablename__ = "counter"
    id = Column(Integer, primary_key=True)
    counter = Column(Integer, default=0)


def setup():
    Base.metadata.create_all(engine)
    if db_session.query(Counter).first() is None:
        db_session.add(Counter(counter=0))
        db_session.commit()


@app.route("/")
def index():
    db_session.add(Counter(counter=0))
    db_session.commit()
    return "OK"
    # counter_obj: Counter = db_session.query(Counter).with_for_update().first()
    # assert counter_obj is not None
    # counter_obj.counter += 1
    # db_session.commit()
    # return f"Counter: {counter_obj.counter}"


# with app.app_context():
#     setup()


if __name__ == "__main__":
    app.run(debug=True)
