import React from "react";
import { Link, Navigate } from "react-router-dom";
import { useTheme } from '@mui/material/styles';
import Dropdownbar from "../components/Dropdownbar"
import { useState, useMemo } from "react";
import { useEffect } from "react";



const Homepage = ({loggedin, setLoggedin}) => {

      return (
        <div>
          {loggedin?
          <div>
          <p>Hi</p>
          <Dropdownbar></Dropdownbar>
        </div> :

        <Navigate to="/login" />
          }
        </div>
      )
      
  
};

export default Homepage;
