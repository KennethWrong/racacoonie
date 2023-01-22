import React, { useEffect, useState } from 'react';
import RecipeCards from './RecipeCards';
import { getAllRecipes } from '../api/api';
import './Recipe.css';

const RecipeBoard = (props) => {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    getAllRecipes().then((res) => {
      setRecipes(res.data.recipes);
    }).catch(e => { console.log(e); });
  }, []);

  return (
    <>
      {recipes ? <RecipeCards recipes={recipes} /> : null}
    </>
  );
};

export default RecipeBoard;
