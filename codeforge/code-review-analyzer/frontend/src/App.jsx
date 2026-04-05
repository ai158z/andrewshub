import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import RepositoryList from './components/RepositoryList';
import AnalysisReport from './components/AnalysisReport';

const App = () => {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li>
              <a href="/">Home</a>
            </li>
            <li>
              <a href="/repositories">Repositories</a>
            </li>
          </ul>
        </nav>
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/repositories" element={<RepositoryList />} />
            <Route path="/report/:reportId" element={<AnalysisReport />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;