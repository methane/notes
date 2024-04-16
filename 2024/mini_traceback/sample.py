import traceback
import sqlalchemy


def main():
    try:
        engine = sqlalchemy.create_engine("sqlite:////bin/hoge.db")
        conn = engine.connect()
        conn.close()
    except Exception as e:
        print("# stdlib traceback")
        s = "".join(traceback.format_exception(e, chain=False))
        print(s)


main()
