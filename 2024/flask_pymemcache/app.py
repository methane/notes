from flask import Flask
from flask_pymemcache import FlaskPyMemcache


app = Flask(__name__)
app.config.from_pyfile('config.py')

cache = FlaskPyMemcache()
cache.init_app(app)

@app.route('/')
def hello():
    cache.client.set(b"foo", b"hello")
    ret = cache.client.get(b"foo")
    print(ret)
    return ret

app.run(debug=True)
