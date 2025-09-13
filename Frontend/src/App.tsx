import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css'
import HomePage from './pages/HomePage'
import DownloadPage from './pages/DownloadPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/download" element={<DownloadPage />} />
      </Routes>
    </Router>
  );
}

export default App