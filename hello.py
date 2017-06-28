from flask import render_template
from flask import redirect
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return '<h1>Hello World!</h1>'

@app.route('/hi/')
@app.route('/hi/<name>')
def hi(name=None):
    return render_template('hi.html', name=name)


@app.route('/user/<name>')
def user(name):
    return redirect('http://www.cnn.com')
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)

