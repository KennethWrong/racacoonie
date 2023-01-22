import React, { useState, useMemo, useEffect } from 'react';
import { Link, Navigate } from 'react-router-dom';

import Dropdownbar from '../components/Dropdownbar';
import RecipeCards from '../components/RecipeCards';
import './Homepage.css';

const Homepage = ({ loggedin, setLoggedin }) => {
  const [recipes, setRecipes] = useState([]);
  return (
    <div>

      {loggedin
        ? (
          <>
            <p>Hi</p>
            <Dropdownbar recipes={recipes} setRecipes={setRecipes} />
            <RecipeCards recipes={recipes} />
          </>
          )

        : <Navigate to='/login' />}
    </div>
  );
};

export default Homepage;
