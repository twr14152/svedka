from flask.ext.script import Manager
from flask import Flask, render_template
from flask import request
from flask import make_response
from flask import redirect
from flask import abort


app = Flask(__name__)
manager = Manager(app)

#@app.route('/')
#def index():
#    return '<h1>Test web page</h1>'
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


#def index():
#    user_agent = request.headers.get('User-Agent')
#    return '<p> Your browser is %s </p>' % user_agent
#    response = make_response('<h1>This document carriers a cookie!</h1>')
#    response.set_cookie('answer', '42')
#    return response
#    return redirect('http://www.cnn.com')
#@app.route('/user/<name>')
#def user(name):
#    return '<h1>Hello, %s!</h1>' % name

#@app.route('/user/<id>')
#def get_user(id):
#    user = load_user(id)
#    if not user:
#        abort(404)
 #   return '<h1>Hello, %s </h1>' % user.name

if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
