import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import { useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import { tableBodyClasses } from '@mui/material';

import FormHelperText from '@mui/material/FormHelperText';
import axios from 'axios';
import TextField from '@mui/material/TextField';

import IngredientsDropdown from './IngredientsDropdown';
import TagsDropdown from './TagsDropdown';
import { getAllIngredients, getAllTags } from '../api/api';
import Dropdown from './Dropdown';

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

const ingredientsArray = ['Apple', 'Onion', 'Grapes', 'Tea'];

const tagsArray = ['Italian', 'French', 'Easy', 'Boy'];

function getStyles (name, personName, theme) {
  return {
    fontWeight:
      personName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium
  };
}

export default function Dropdownbar (props) {
  const theme = useTheme();

  const [uniqueIngredients, setUniqueIngredients] = useState([]);
  const [uniqueTags, setUniqueTags] = useState([]);

  const [ingredients, setIngredients] = useState([]);
  const [minutes, setminutes] = useState('');
  const [tags, setTags] = useState([]);
  const [searchbar, setSearchBar] = useState('');

  useEffect(() => {
    getAllIngredients().then((res) => {
      setUniqueIngredients(res.data.ingredients);
      // console.log(res.data.ingredients);
    }).catch(e => { console.log(e); });

    getAllTags().then((res) => {
      setUniqueTags(res.data.tags);
      // console.log(res.data.tags);
    }).catch(e => { console.log(e); });
  }, []);

  const getRecipeByFilter = (e) => {
    e.preventDefault();
    try {
      console.log(
        {
          ingredients: ingredients,
          minutes: minutes,
          tags: tags,
          search: searchbar
        }
      );
      axios.post('http://localhost:8000/recipe/filter', {
        ingredients: ingredients,
        minutes: minutes,
        tags: tags,
        search: searchbar
      }).then(
        (res) => {
          console.log(res)
          console.log(res.data.recipes);
          props.setRecipes(res.data.recipes);
        }
      );
    } catch (e) {

    }
  };

  const handleMinutesChange = (event) => {
    setminutes(event.target.value);
  };

  const handleSearchChange = (event) => {
    setSearchBar(event.target.value);
  };

  const [hideDropdown, setHideDropdown] = useState(false);
  const toggleDropdown = () => {
    setHideDropdown(prevHideDropdown => !prevHideDropdown);
  };

  return (
    <div>
      <button className='toggle-button' onClick={toggleDropdown}>Toggle</button>
      {hideDropdown
        ? (
          <>
            <div className='filter-container'>
              <Dropdown className='dropdown' name='Ingredients:' items={uniqueIngredients} selected={ingredients} setState={setIngredients} />
              <Dropdown className='dropdown' name='Tags:' items={uniqueTags} selected={tags} setState={setTags} />
            </div>
            <input className='search-bar' placeholder='Enter max cook-time (mins)' onChange={handleMinutesChange} />
          </>
          )
        : null}

      <input className='search-bar' placeholder='Search Recipe' onChange={handleSearchChange} />
      <button type='submit' onClick={getRecipeByFilter}>Filter</button>
    </div>
  );
}
