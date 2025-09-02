#!/bin/bash

# .venv ディレクトリがなかったら作る
if [ ! -d .venv ]; then
    uv venv
    uv pip install uwsgi
fi

# uwsgiをバックグラウンドで起動
.venv/bin/uwsgi --http-socket :4321 --enable-threads --module wsgi --callable application --lazy-app --threads=4 --die-on-term --master --pidfile uwsgi.pid -d uwsgi.log

for i in {0..50}
do
    curl http://127.0.0.1:4321/
    echo
done

kill -TERM $(cat uwsgi.pid)
