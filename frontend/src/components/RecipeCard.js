import React from 'react';
import './Recipe.css';
import { useNavigate } from 'react-router-dom';

const RecipeCard = (props) => {
  const navigate = useNavigate();
  return (
    <div className='recipe-card g-g-col-4' onClick={() => { navigate('/recipe/' + props.recipe.id); }}>
      <div className='recipe-image'>
        image
      </div>
      <div className='recipe-details'>
        <p className='recipe-name'>{props.recipe.name}</p>
        <hr className='recipe-hr' />
        <p className='recipe-description'>{props.recipe.description}</p>
      </div>

    </div>
  );
};

export default RecipeCard;
