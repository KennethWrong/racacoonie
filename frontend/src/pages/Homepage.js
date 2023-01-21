import React from "react";
import { Link, Navigate } from "react-router-dom";
import { useTheme } from '@mui/material/styles';
import Dropdownbar from "../components/Dropdownbar"
import { useState } from "react";
import { useMemo } from "react";



const Homepage = () => {
    const [loggedin, setLoggedin] = useState(false);
    const [hi, sethi] = useState(false)

    // useMemo(() => {
    //   var authToken = localStorage.getItem("racacoonie-auth-token");

    //     // storing input name
    //     if (authToken) {
    //         setLoggedin(true);
    //     }
        
    //   }, []);// Navbar and routing on first open

        return (
            <div>
              <Dropdownbar></Dropdownbar>
            </div>
          );
  
      
  
};

export default Homepage;
