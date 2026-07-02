import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

import TodoItem from '@/components/TodoItem/TodoItem';

const todo = { id: 1, title: 'Buy groceries', completed: false };

describe('TodoItem', () => {
  it('renders the task title', () => {
    render(<TodoItem todo={todo} toggleTodo={vi.fn()} deleteTodo={vi.fn()} />);
    expect(screen.getByText('Buy groceries')).toBeInTheDocument();
  });

  it('calls toggleTodo with the correct id when checkbox is checked', () => {
    const toggleTodo = vi.fn();
    render(<TodoItem todo={todo} toggleTodo={toggleTodo} deleteTodo={vi.fn()} />);
    fireEvent.click(screen.getByRole('checkbox'));
    expect(toggleTodo).toHaveBeenCalledWith(1);
  });

  it('calls deleteTodo with the correct id when delete is clicked', () => {
    const deleteTodo = vi.fn();
    render(<TodoItem todo={todo} toggleTodo={vi.fn()} deleteTodo={deleteTodo} />);
    fireEvent.click(screen.getByText('Delete'));
    expect(deleteTodo).toHaveBeenCalledWith(1);
  });
});
