# Needed to utilize files in templates folder
from flask import render_template
# Used for redirect app.route
from flask import redirect
# Needed for flask in general
from flask import Flask

app = Flask(__name__)

# http://a.b.c.d:####/
@app.route('/')
def index():
    return 'Index Page'

# http://a.b.c.d:####/hello
@app.route('/hello')
def hello():
    return '<h1>Hello World!</h1>'

# http://a.b.c.d:####/hi (uses templates)
# http://a.b.c.d:####/hi/test (uses templates)  
@app.route('/hi/')
@app.route('/hi/<name>')
def hi(name=None):
    return render_template('hi.html', name=name)

# http://a.b.c.d:####/user/test -->redirect to cnn.com
@app.route('/user/<name>')
def user(name):
    return redirect('http://www.cnn.com')
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)

