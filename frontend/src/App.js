import './App.css';
import {BrowserRouter, Route, Routes } from 'react-router-dom'
import Login from './pages/Login'
import { useState, useEffect, useMemo } from "react";
import Homepage from './pages/Homepage';
import NavbarComponent from './components/Navbar';

function App() {
  const [loggedin, setLoggedin] = useState(false)

  useMemo(() => {
    // storing input name
    var authToken = localStorage.getItem("racacoonie-auth-token");
    if (authToken) {
        setLoggedin(true);
    }
    
  }, []);// Navbar and routing on first open
  
  return (
    <div className="App">     
          <BrowserRouter>
            <NavbarComponent loggedin={loggedin}/>
            <Routes>
              <Route path ='/' element={<Homepage loggedin={loggedin} setLoggedin={setLoggedin}/>} />
              <Route path ='/login' element={<Login loggedin={loggedin} setLoggedin={setLoggedin}/>} />
            </Routes>
          </BrowserRouter>
          </div>
  );
}

export default App;
