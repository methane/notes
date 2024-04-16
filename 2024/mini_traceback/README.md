# sample for long traceback

```
# stdlib traceback
Traceback (most recent call last):
  File "/Users/inada-n/notes/2024/mini_traceback/sample.py", line 8, in main
    conn = engine.connect()
           ^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3280, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 148, in __init__
    Connection._handle_dbapi_exception_noconnection(
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 2444, in _handle_dbapi_exception_noconnection
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 146, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3304, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 449, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1263, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 179, in _do_get
    with util.safe_reraise():
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 390, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 674, in __init__
    self.__connect()
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 900, in __connect
    with util.safe_reraise():
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 896, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/engine/create.py", line 643, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/inada-n/notes/2024/mini_traceback/.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 617, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file
(Background on this error at: https://sqlalche.me/e/20/e3q8)
```
