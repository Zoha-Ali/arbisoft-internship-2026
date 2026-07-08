import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';

import { Todo } from '@/types';
import { BASE_URL } from '@/utils/constants';
import TodoForm from '@/components/TodoForm/TodoForm';
import TodoList from '@/components/TodoList/TodoList';

const Todos = () => {
  const [todos, setTodos] = useState<Todo[]>([]);

  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const res = await fetch(`${BASE_URL}/todos`);
        const data = await res.json();
        setTodos(data);
      } catch {
        toast.error('Failed to load todos.');
      }
    };

    fetchTodos();
  }, []);

  const addTodo = async (title: string) => {
    try {
      const res = await fetch(`${BASE_URL}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      });
      const created = await res.json();
      setTodos((prev) => [...prev, created]);
      toast.success('Todo added!');
    } catch {
      toast.error('Failed to add todo.');
    }
  };

  const toggleTodo = async (id: number) => {
    const todo = todos.find((t) => t.id === id);
    if (!todo) return;

    try {
      const res = await fetch(`${BASE_URL}/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !todo.completed }),
      });
      const updated = await res.json();
      setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
    } catch {
      toast.error('Failed to update todo.');
    }
  };

  const deleteTodo = async (id: number) => {
    try {
      await fetch(`${BASE_URL}/todos/${id}`, { method: 'DELETE' });
      setTodos((prev) => prev.filter((t) => t.id !== id));
      toast.success('Todo deleted!');
    } catch {
      toast.error('Failed to delete todo.');
    }
  };

  return (
    <section>
      <h1>Todos</h1>
      <TodoForm addTodo={addTodo} />
      <TodoList todos={todos} toggleTodo={toggleTodo} deleteTodo={deleteTodo} />
    </section>
  );
};

export default Todos;
