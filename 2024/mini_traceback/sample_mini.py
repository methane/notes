import minitraceback
import sqlalchemy


def main():
    try:
        engine = sqlalchemy.create_engine("sqlite:////bin/hoge.db")
        conn = engine.connect()
        conn.close()
    except Exception as e:
        print("# minitraceback")
        minitraceback.print_exception(e)


main()
