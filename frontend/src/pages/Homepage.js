import React, { useState, useMemo, useEffect } from 'react';
import { Link, Navigate } from 'react-router-dom';

import Dropdownbar from '../components/Dropdownbar';
import RecipeCards from '../components/RecipeCards';
import './Homepage.css';
import { getForYouRecipes } from '../api/api';

const Homepage = ({ loggedin, setLoggedin }) => {
  const [recipes, setRecipes] = useState([]);

  const [forYouRecipes, setForYouRecipes] = useState([]);
  useEffect(() => {
    getForYouRecipes().then((res) => {
      const topRecipes = [];
      res.data.recommendations.forEach(user => {
        topRecipes.extend(user.recipes);
      });

      setForYouRecipes(topRecipes);
    }).catch();
  }, []);

  return (
    <div>

      {loggedin
        ? (
          <>
            <Dropdownbar recipes={recipes} setRecipes={setRecipes} />
            <RecipeCards recipes={recipes} />

            <h1>Recipes For You</h1>
            <RecipeCards recipes={forYouRecipes} />
          </>
          )

        : <Navigate to='/login' />}
    </div>
  );
};

export default Homepage;
