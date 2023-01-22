import React from 'react';
import './Recipe.css';
import { useNavigate } from 'react-router-dom';

const RecipeCards = (props) => {
  const navigate = useNavigate();
  return (
    <div className='recipe-board'>
      {props.recipes
        ? props.recipes.map((recipe) => (
          <div key={recipe.id} className='recipe-card g-g-col-4' onClick={() => { navigate('/recipe/' + recipe.id); }}>
            <div className='recipe-image'>
              image
            </div>
            <div className='recipe-details'>
              <p className='recipe-name'>{recipe.name}</p>
              <hr className='recipe-hr' />
              <p className='recipe-description'>{recipe.description}</p>
            </div>
          </div>
          ))
        : null}
    </div>

  );
};

export default RecipeCards;
