interface Todo {
  id: number;
  title: string;
  completed: boolean;
}

interface Props {
  todo: Todo;
  toggleTodo: (id: number) => void;
  deleteTodo: (id: number) => void;
}

export default function TodoItem({ todo, toggleTodo, deleteTodo }: Props) {
  return (
    <li className="todo-item">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => toggleTodo(todo.id)}
      />
      <span className={`todo-item__title${todo.completed ? ' todo-item__title--completed' : ''}`}>
        {todo.title}
      </span>
      <button className="todo-item__delete" onClick={() => deleteTodo(todo.id)}>
        Delete
      </button>
    </li>
  );
}
