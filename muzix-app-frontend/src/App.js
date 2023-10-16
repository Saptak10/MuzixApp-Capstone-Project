import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import MusicPlayer from './components/MusicPlayer';
import PageNotfound from './components/PageNotfound';

function App() {
  return (
    <Router className="App">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<PageNotfound />} />
      </Routes>
      <MusicPlayer />
    </Router>
  );
}

export default App;
