import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

import { useAuth } from '@/contexts/AuthContext/AuthContext';
import { Todo } from '@/types';
import { BASE_URL } from '@/utils/constants';
import TodoForm from '@/components/TodoForm/TodoForm';
import TodoList from '@/components/TodoList/TodoList';

const Todos = () => {
  const { accessToken, isLoading } = useAuth();
  const navigate = useNavigate();
  const [todos, setTodos] = useState<Todo[]>([]);

  const authHeaders = (): HeadersInit => ({
    'Content-Type': 'application/json',
    ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
  });

  useEffect(() => {
    if (isLoading) return;

    const fetchTodos = async () => {
      try {
        const res = await fetch(`${BASE_URL}/todos`, { headers: authHeaders() });
        if (!res.ok) {
          if (res.status === 401) {
            toast.error('Session expired. Please sign in again.');
            navigate('/signin');
          } else {
            toast.error('Failed to load todos.');
          }
          return;
        }
        const data = await res.json();
        setTodos(data);
      } catch {
        toast.error('Failed to load todos.');
      }
    };

    fetchTodos();
  }, [accessToken, isLoading]);

  const addTodo = async (title: string) => {
    try {
      const res = await fetch(`${BASE_URL}/todos`, {
        method: 'POST',
        headers: authHeaders(),
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
        headers: authHeaders(),
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
      await fetch(`${BASE_URL}/todos/${id}`, { method: 'DELETE', headers: authHeaders() });
      setTodos((prev) => prev.filter((t) => t.id !== id));
      toast.success('Todo deleted!');
    } catch {
      toast.error('Failed to delete todo.');
    }
  };

  if (isLoading) return <p>Loading...</p>;

  return (
    <section>
      <h1>Todos</h1>
      <TodoForm addTodo={addTodo} />
      <TodoList todos={todos} toggleTodo={toggleTodo} deleteTodo={deleteTodo} />
    </section>
  );
};

export default Todos;
