import './TodoList.css';
import { Todo } from '../../types';
import TodoItem from '../TodoItem/TodoItem';

interface Props {
  todos: Todo[];
  toggleTodo: (id: number) => void;
  deleteTodo: (id: number) => void;
}

const TodoList = ({ todos, toggleTodo, deleteTodo }: Props) => {
  if (todos.length === 0) return <p className="todo-empty">No todos yet.</p>;

  return (
    <ul className="todo-list">
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} toggleTodo={toggleTodo} deleteTodo={deleteTodo} />
      ))}
    </ul>
  );
};

export default TodoList;
