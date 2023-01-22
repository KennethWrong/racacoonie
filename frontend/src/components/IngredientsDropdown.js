import React, { useEffect, useState } from 'react';
import { getAllIngredients } from '../api/api.js';
import { FormControl, MenuItem, InputLabel, OutlinedInput, Select, Chip, Box } from '@mui/material';
// import Input from './Input';
// import { useForm } from 'react-hook-form';
// import { ErrorMessage } from '@hookform/error-message';
import { useTheme } from '@mui/material/styles';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250
    }
  }
};

function getStyles (theme) {
  return {
    fontWeight: theme.typography.fontWeightRegular
  };
}

const IngredientsDropdown = (props) => {
  const theme = useTheme();

  const [ingredients, setIngredients] = useState([]);
  useEffect(() => {
    getAllIngredients().then((res) => {
      setIngredients(res.data.ingredients);
      console.log(res.data.ingredients);
    }).catch(e => { console.log(e); });
  }, []);

  return (
    <div className='w-full px-3 mb-8'>
      <label
        className='form-label block text-gray-800 text-sm font-medium mb-1'
        htmlFor='ingredients'
      >
        Ingredients<span className='text-red-600'>*</span>
      </label>
      <select
        name='ingredients'
        className='form-select w-full focus:outline-none'
        onChange={props.changeHandler}
        multiple
      >
        <option value='' disabled defaultValue>
          Select your Ingredients
        </option>

        {ingredients ? ingredients.map((ingredient) => (
          <option key={ingredient.id} value={ingredient.id}>{ingredient.name}</option>
        )) : null}

      </select>
      {/* <p className='block text-sm font-medium text-red-600'>
      <ErrorMessage errors={props.errors} name='category' />
    </p> */}
    </div>
  );
};

export default IngredientsDropdown;
