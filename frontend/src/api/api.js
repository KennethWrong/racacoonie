import racaApp from './Axios.js';

export const getAllIngredients = async () => {
  return racaApp.get('/ingredient/all', {
    headers: {
      Authorization: localStorage.getItem('racacoonie-auth-token')
    }
  });
};

export const getAllTags = async () => {
  return racaApp.get('/tag/all', {
    headers: {
      Authorization: localStorage.getItem('racacoonie-auth-token')
    }
  });
};

// export const getRecipe
export const getAllRecipes = async () => {
  return racaApp.get('/recipe/all', {
    headers: {
      Authorization: localStorage.getItem('racacoonie-auth-token')
    }
  });
};
