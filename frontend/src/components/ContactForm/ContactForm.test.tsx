import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

import ContactForm from '@/components/ContactForm/ContactForm';

describe('ContactForm', () => {
  it('renders name and email fields', () => {
    render(<ContactForm onSubmit={vi.fn()} />);
    expect(screen.getByLabelText('Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
  });

  it('shows validation errors on empty submit', () => {
    render(<ContactForm onSubmit={vi.fn()} />);
    fireEvent.click(screen.getByText('Send'));
    expect(screen.getByText('Name is required')).toBeInTheDocument();
    expect(screen.getByText('Email is required')).toBeInTheDocument();
  });

  it('rejects an invalid email', () => {
    render(<ContactForm onSubmit={vi.fn()} />);
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Zoha' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'not-an-email' } });
    fireEvent.click(screen.getByText('Send'));
    expect(screen.getByText('Enter a valid email')).toBeInTheDocument();
  });

  it('calls onSubmit with valid data', () => {
    const onSubmit = vi.fn();
    render(<ContactForm onSubmit={onSubmit} />);
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Zoha' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'zoha@example.com' } });
    fireEvent.click(screen.getByText('Send'));
    expect(onSubmit).toHaveBeenCalledWith({ name: 'Zoha', email: 'zoha@example.com' });
  });
});
