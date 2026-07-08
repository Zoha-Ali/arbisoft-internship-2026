import { Routes, Route } from 'react-router-dom';

import Layout from '@/components/Layout/Layout';
import Home from '@/routes/Home/Home';
import About from '@/routes/About/About';
import SignUp from '@/routes/SignUp/SignUp';
import Todos from '@/routes/Todos/Todos';

const App = () => {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="about" element={<About />} />
        <Route path="todos" element={<Todos />} />
        <Route path="signup" element={<SignUp />} />
      </Route>
    </Routes>
  );
};

export default App;
