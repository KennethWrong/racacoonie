import './App.css';
import { BrowserRouter, Route, Routes, Navigate, useParams } from 'react-router-dom';
import Login from './pages/Login';
import React, { useState, useEffect, useMemo } from 'react';
import Homepage from './pages/Homepage';
import NavbarComponent from './components/Navbar';
import Recipe from './pages/Recipe';

function App () {
  const [loggedin, setLoggedin] = useState(false);

  useMemo(() => {
    // storing input name
    const authToken = localStorage.getItem('racacoonie-auth-token');
    if (authToken) {
      setLoggedin(true);
    }
  }, []);// Navbar and routing on first open

  return (
    <div className='App'>
      <BrowserRouter>
        <NavbarComponent loggedin={loggedin} setLoggedin={setLoggedin} />
        <Routes>
          <Route path='/' element={<Homepage loggedin={loggedin} setLoggedin={setLoggedin} />} />
          <Route
            path='/login' element={
                loggedin ? <Navigate to='/' />
                  : <Login loggedin={loggedin} setLoggedin={setLoggedin} />
}
          />
          <Route
            path='/recipe/:rid' element={<Recipe />}
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
