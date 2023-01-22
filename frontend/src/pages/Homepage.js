import React, { useState, useMemo, useEffect } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { useTheme } from '@mui/material/styles';
import Dropdownbar from '../components/Dropdownbar';
import RecipeBoard from '../components/RecipeBoard';

const Homepage = ({ loggedin, setLoggedin }) => {
  return (
    <div>
      {loggedin
        ? (
          <>
            <p>Hi</p>
            {/* <Dropdownbar /> */}
            <RecipeBoard />
          </>
          )

        : <Navigate to='/login' />}
    </div>
  );
};

export default Homepage;
