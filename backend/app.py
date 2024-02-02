from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
CORS(app)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todos.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)


db.create_all()


@app.route('/todos', methods=['GET', 'POST'])
def manage_todos():
    if request.method == 'GET':
        todos = Todo.query.all()
        return jsonify([{'id': todo.id, 'title': todo.title, 'completed': todo.completed} for todo in todos])
    elif request.method == 'POST':
        data = request.get_json()
        new_todo = Todo(title=data['title'])
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({'id': new_todo.id, 'title': new_todo.title, 'completed': new_todo.completed}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
def update_delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if request.method == 'PUT':
        data = request.get_json()
        todo.title = data.get('title', todo.title)
        todo.completed = data.get('completed', todo.completed)
        db.session.commit()
        return jsonify({'id': todo.id, 'title': todo.title, 'completed': todo.completed})
    
    if request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo deleted'})


if __name__ == '__main__':
    app.run(debug=True)
