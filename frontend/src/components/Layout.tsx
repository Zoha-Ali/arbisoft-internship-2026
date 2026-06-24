import { Link, Outlet } from 'react-router-dom';

export default function Layout() {
  return (
    <div className="app-shell">
      <nav className="nav">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/todos">Todos</Link>
      </nav>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
