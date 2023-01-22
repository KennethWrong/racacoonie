import React, { useState, useMemo, useEffect } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { useTheme } from '@mui/material/styles';
import Dropdownbar from '../components/Dropdownbar';

const Homepage = ({ loggedin, setLoggedin }) => {
  return (
    <div>
      {loggedin
            ? <div>
              <p>Hi</p>
              <Dropdownbar />
              </div>

            : <Navigate to='/login' />}
    </div>
  );
};

export default Homepage;
