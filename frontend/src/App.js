import './App.css';
import { BrowserRouter, Route, Routes, Navigate, useParams } from 'react-router-dom';
import Login from './pages/Login';
import React, { useState, useEffect, useMemo } from 'react';
import Homepage from './pages/Homepage';
import NavbarComponent from './components/Navbar';
<<<<<<< HEAD
import Recipe from './pages/Recipe'
import Saved from './pages/Saved'

=======
import Recipe from './pages/Recipe';
>>>>>>> 1bd775ee1a6f68bc3fea4fb802c797216e866db3

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
<<<<<<< HEAD
              <Route path='/recipe/:rid' element={<Recipe />}/>
              <Route path='/saved' element={loggedin ? <Saved /> 
                          : <Login loggedin={loggedin} setLoggedin={setLoggedin}/>}/>
            </Routes>

          </BrowserRouter>
=======
          <Route
                path='/recipe/:rid' element={<Recipe />}
              />
        </Routes>
      </BrowserRouter>
>>>>>>> 1bd775ee1a6f68bc3fea4fb802c797216e866db3
    </div>
  );
}

export default App;
