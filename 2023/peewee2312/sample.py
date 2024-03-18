import peewee as pw


db = pw.MySQLDatabase('testdb',
                    user='testdb',
                    #password='',
                    host='127.0.0.1',
                    port=3306)

# db = pw.SqliteDatabase('people.db')

class BaseModel(pw.Model):
    class Meta:
        database = db

class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()


class Tweet(BaseModel):
    user = pw.ForeignKeyField(User, backref='tweets')
    message = pw.TextField()
    created_date = pw.DateTimeField()

db.connect()
db.create_tables([User, Tweet])
