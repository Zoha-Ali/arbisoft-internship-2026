import { useForm } from 'react-hook-form';

import './TodoForm.css';

interface Props {
  addTodo: (title: string) => void;
}

interface FormValues {
  title: string;
}

const TodoForm = ({ addTodo }: Props) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormValues>();

  const onSubmit = (data: FormValues) => {
    addTodo(data.title.trim());
    reset();
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit(onSubmit)}>
      <input
        type="text"
        placeholder="New task..."
        {...register('title', {
          required: 'Task title cannot be empty.',
          validate: (value) => value.trim().length > 0 || 'Task title cannot be only spaces.',
          pattern: {
            value: /^[a-zA-Z0-9\s.,!?'-]+$/,
            message: 'Title contains invalid special characters.',
          },
        })}
      />
      <button type="submit">Add</button>
      {errors.title && <p className="form-error">{errors.title.message}</p>}
    </form>
  );
};

export default TodoForm;
