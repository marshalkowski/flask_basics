from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(
    SECRET_KEY='supersecure',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:PostReal1ty@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False)

db = SQLAlchemy(app)


@app.route('/index')
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/new/')
def query_strings(greeting = 'Hey, there'):
    query_val = request.args.get('greeting', greeting)
    return '<h1>Greeting is: {0} </hq>'.format(query_val)


@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='Cecilia'):
    return '<h1>Hello, {}!</h1>'.format(name)


# TEMPLATES
@app.route('/temp')
def using_templates():
    return render_template('hello.html')


# JINJA TEMPLATES
@app.route('/todo')
def tasks_to_do():
    task_list = ['fix fence',
                 'build workbench',
                 'move powerstrip',
                 'adjust desk',
                 'organize office']

    return render_template('todolist.html',
                           tasks=task_list,
                           name='Ben')


@app.route('/bye')
def bye_moon():
    return 'Goodbye Moon!'


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format(self.id, self.name)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    #Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

