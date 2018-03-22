from app.catalog import main

@main.route('/')
def hello():
    return 'hello, world'


@main.route('/goodbye')
def bye():
    return 'goodbye, all!'
