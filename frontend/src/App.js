import './App.css';
import {BrowserRouter, Route, Routes } from 'react-router-dom'
import Login from './pages/Login'
import Homepage from './pages/Homepage';
import NavbarComponent from './components/Navbar';

function App() {
  return (
    <div className="App">     
              
          <BrowserRouter>
          <NavbarComponent />
          <Routes>
           <Route path ='/' element={<Homepage/>} />
           <Route path ='/login' element={<Login/>} />
          </Routes>
          </BrowserRouter>
          </div>
  );
}

export default App;
