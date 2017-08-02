# Needed to utilize files in templates folder
from flask import render_template
# Used for redirect app.route
from flask import redirect
# Needed for flask in general
from flask import Flask
# Needed for flask requests
from flask import request
# Used for error handling
from flask import abort

app = Flask(__name__)

# http://a.b.c.d:####/
@app.route('/')
def index():
    return 'Index Page'

# http://a.b.c.d:####/hello
@app.route('/hello')
def hello():
    return '<h1>Hello World!</h1>'

# variable urls
# http://a.b.c.d:####/hello_again/sam
@app.route('/hello_again/<name>')
def hello_again(name):
    return 'Hello again %s!' % name

# http://a.b.c.d:####/hi (uses templates)
# http://a.b.c.d:####/hi/test (uses templates)  
@app.route('/hi/')
@app.route('/hi/<name>')
def hi(name=None):
    return render_template('hi.html', name=name)

# http://a.b.c.d:####/user/test -->redirect to cnn.com
@app.route('/user1/<name>')
def user1(name):
    return redirect('http://www.cnn.com')
    return '<h1>Hello, %s!</h1>' % name

# http://a.b.c.d:####/test/
# This request will tell you all about your browser
@app.route('/test/')
def test():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent

# Used to demonstrate abort(error handling)
# Not working. Load user not defined. 
@app.route('/user/<id>')
def user(id):
    user = load_user(id)
    if not user:
         abort(404)
    return '<h1>Hello, %s</h1>' % user.name


if __name__ == '__main__':
    #allows other devices to access this service
    app.run(debug = True,host="0.0.0.0")
