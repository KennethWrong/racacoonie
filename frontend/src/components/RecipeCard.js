import React from 'react';

const RecipeCard = (props) => {
  return (
  // <div className='text-red bg-amber-600 w-1/4 rounded-md drop-shadow-lg m-0'>

    <div className='font-red'>
      {props.recipe.name}
    </div>
  );
};

export default RecipeCard;
