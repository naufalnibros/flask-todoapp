from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/flask_todoapp'

db = SQLAlchemy(app)

class Todo(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    text            = db.Column(db.String(200))
    is_complete     = db.Column(db.Boolean)

@app.route('/')
def index():
    incomplete = Todo.query.filter_by(is_complete=False).all()
    complete   = Todo.query.filter_by(is_complete=True).all()
    return render_template('index.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todo'], is_complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.is_complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/incomplete/<id>')
def incomplete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.is_complete = False
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
