import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Landing from './pages/Landing';
import Editor from './pages/Editor';
import About from './pages/About';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-background text-body font-sans">
        <Navbar />
        <main className="flex-grow flex flex-col">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/editor" element={<Editor />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
