import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AboutUs from './AboutUs.jsx';
import Home from './Home.jsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/aboutus" element={<AboutUs />} />
        <Route path="/" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
