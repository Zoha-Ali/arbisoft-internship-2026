import { useState, FormEvent } from 'react';

export interface ContactFormData {
  name: string;
  email: string;
}

interface ContactFormProps {
  onSubmit: (data: ContactFormData) => void;
}

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function ContactForm({ onSubmit }: ContactFormProps) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [errors, setErrors] = useState<{ name?: string; email?: string }>({});

  function validate(): boolean {
    const next: { name?: string; email?: string } = {};
    if (!name.trim()) next.name = 'Name is required';
    if (!email.trim()) next.email = 'Email is required';
    else if (!EMAIL_REGEX.test(email)) next.email = 'Enter a valid email';
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (validate()) {
      onSubmit({ name, email });
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <label htmlFor="name">Name</label>
      <input id="name" value={name} onChange={(e) => setName(e.target.value)} />
      {errors.name && <p role="alert">{errors.name}</p>}

      <label htmlFor="email">Email</label>
      <input id="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      {errors.email && <p role="alert">{errors.email}</p>}

      <button type="submit">Send</button>
    </form>
  );
}
