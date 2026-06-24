import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './routes/Home';
import About from './routes/About';
import Todos from './routes/Todos';

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="about" element={<About />} />
        <Route path="todos" element={<Todos />} />
      </Route>
    </Routes>
  );
}
