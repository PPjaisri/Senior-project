import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Result from './pages/Result';
import Search from './pages/Search';

function App() {
  return (
    <div>
      <Routes>
        <Route path='/' element={<Search />} />
        <Route path='/result' element={<Result />} />
      </Routes>
    </div>
  );
}

export default App;
