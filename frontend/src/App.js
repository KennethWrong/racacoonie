import './App.css';
import {BrowserRouter, Route, Routes, Navigate} from 'react-router-dom'
import Login from './pages/Login'
import Homepage from './pages/Homepage';
import NavbarComponent from './components/Navbar';
import { useState, useMemo, useEffect } from "react";


function App() {
  const [loggedin, setLoggedin] = useState(false);


  useEffect(() => {
    var authToken = localStorage.getItem("racacoonie-auth-token");
    // storing input name
    if (authToken) {
        setLoggedin(true);
    }

    
    
  }, [loggedin]);// Navbar and routing on first open
  
  return (
    <div className="App">     
          <BrowserRouter>
            <NavbarComponent />
            <Routes>
              <Route path ='/' element={loggedin ? <Homepage />: <Homepage />} />
              <Route path ='/login' element={loggedin ? <Navigate to="/" /> : <Login/>} />
            </Routes>
          </BrowserRouter>
          </div>
  );
}

export default App;
