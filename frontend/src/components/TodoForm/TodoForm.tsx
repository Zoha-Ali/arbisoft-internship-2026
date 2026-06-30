import { useState } from 'react';
import './TodoForm.css';

interface Props {
  addTodo: (title: string) => void;
}

const TodoForm = ({ addTodo }: Props) => {
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Task title cannot be empty.');
      return;
    }
    addTodo(title.trim());
    setTitle('');
    setError('');
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="New task..."
      />
      <button type="submit">Add</button>
      {error && <p className="form-error">{error}</p>}
    </form>
  );
};

export default TodoForm;