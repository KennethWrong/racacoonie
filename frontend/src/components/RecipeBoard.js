import React, { useEffect, useState } from 'react';
import RecipeCard from './RecipeCard';
import { getAllRecipes } from '../api/api';

const RecipeBoard = (props) => {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    getAllRecipes().then((res) => {
      setRecipes(res.data.recipes);
    }).catch(e => { console.log(e); });
  }, []);

  return (
    <div className=''>
      {recipes ? recipes.map(recipe => (<RecipeCard key={recipe.id} recipe={recipe} />)) : null}
    </div>
  );
};

export default RecipeBoard;
