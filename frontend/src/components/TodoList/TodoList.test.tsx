import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

import TodoList from '@/components/TodoList/TodoList';

const todos = [
  { id: 1, title: 'Buy groceries', completed: false },
  { id: 2, title: 'Walk the dog', completed: true },
];

describe('TodoList', () => {
  it('renders all todos passed as props', () => {
    render(<TodoList todos={todos} toggleTodo={vi.fn()} deleteTodo={vi.fn()} />);
    expect(screen.getByText('Buy groceries')).toBeInTheDocument();
    expect(screen.getByText('Walk the dog')).toBeInTheDocument();
  });

  it('shows "No todos yet." when the list is empty', () => {
    render(<TodoList todos={[]} toggleTodo={vi.fn()} deleteTodo={vi.fn()} />);
    expect(screen.getByText('No todos yet.')).toBeInTheDocument();
  });
});
