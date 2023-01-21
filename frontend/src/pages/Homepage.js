import React from "react";
import { Link, Navigate } from "react-router-dom";
import { useTheme } from '@mui/material/styles';
import Dropdownbar from "../components/Dropdownbar"
import { useState } from "react";
import { useEffect } from "react";



const Homepage = () => {
    const [loggedin, setLoggedin] = useState(false);

    useEffect(() => {
        // storing input name
        var authToken = localStorage.getItem("racacoonie-auth-token");
        if (authToken) {
            setLoggedin(true);
        }
        
      }, []);// Navbar and routing on first open

      if (loggedin) {
        return (
            <div>
              <p>Hi</p>
              <Dropdownbar></Dropdownbar>
            </div>
          );
      } else {
        return (
            <Navigate to="/login" replace /> 
        )
      }
      
  
};

export default Homepage;
