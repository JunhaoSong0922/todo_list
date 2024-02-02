import React, { useState, useEffect } from 'react';
import './App.css';
import { VegaLite } from 'react-vega';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    const response = await fetch('http://localhost:5000/todos');
    const data = await response.json();
    setTodos(data);
  };

  const addTodo = async () => {
    if (!newTodo.trim()) return;
    const response = await fetch('http://localhost:5000/todos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title: newTodo }),
    });
    if (response.ok) {
      setNewTodo('');
      fetchTodos();
    }
  };

  // Vega
  const chartSpec = {
    $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
    description: 'Todo completion status',
    data: {
      values: todos.map(todo => ({ status: todo.completed ? 'Completed' : 'Not Completed' }))
    },
    mark: 'bar',
    encoding: {
      x: { field: 'status', type: 'nominal', axis: { title: 'Status' }},
      y: { aggregate: 'count', type: 'quantitative', axis: { title: 'Count' }}
    }
  };


  return (
    <div>
      <input
        type="text"
        placeholder="Add new todo"
        value={newTodo}
        onChange={(e) => setNewTodo(e.target.value)}
      />
      <button onClick={addTodo}>Add Todo</button>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
