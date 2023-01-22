import React, { useState } from 'react';
import './Recipe.css';
import { useNavigate } from 'react-router-dom';
import SaveButton from "../components/SaveButton";

const RecipeCards = (props) => {
  const navigate = useNavigate();
  const [showMore, setShowMore] = useState(false);

  return (
    <div className='recipe-board'>
      {props.recipes
        ? props.recipes.map((recipe) => (
          <div key={recipe.id} className='recipe-card g-g-col-4'>
            <div className='recipe-image hover:cursor-pointer' onClick={() => { navigate('/recipe/' + recipe.id); }}>
              image
            </div>
            <div className='recipe-details'>
              <p className='recipe-name'>
                {recipe.name}
              </p>
              <span>
                <SaveButton rid={recipe['id']}/>
              </span>
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
