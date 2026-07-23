import { Link, Outlet, useNavigate } from 'react-router-dom';
import './Layout.css';

import { useAuth } from '@/contexts/AuthContext/AuthContext';

const Layout = () => {
  const { accessToken, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/signin');
  };

  return (
    <div className="app-shell">
      <nav className="nav">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/todos">Todos</Link>
        <Link to="/agent">Agent</Link>
        {accessToken ? (
          <button className="nav-logout" onClick={handleLogout}>Log Out</button>
        ) : (
          <>
            <Link to="/signup">Sign Up</Link>
            <Link to="/signin">Sign In</Link>
          </>
        )}
      </nav>
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
