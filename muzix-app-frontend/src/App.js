import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';
import Home from './components/Home';
import MusicPlayer from './components/MusicPlayer';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Home />
      <MusicPlayer />
    </div>
  );
}

export default App;
