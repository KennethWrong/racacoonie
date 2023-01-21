import * as React from "react";
import { useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Chip from "@mui/material/Chip";
import { useState } from "react";
import Button from "@mui/material/Button";
import { tableBodyClasses } from "@mui/material";
import { useEffect } from "react";
import FormHelperText from '@mui/material/FormHelperText';
import axios from "axios";
import TextField from '@mui/material/TextField';


const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};


const ingredientsArray = ["Apple", "Onion", "Grapes", "Tea"];

const tagsArray = ["Italian", "French", "Easy", "Boy"];

function getStyles(name, personName, theme) {
  return {
    fontWeight:
      personName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}

export default function Dropdownbar() {
  const theme = useTheme();
  const [dbIngredient, setdbIngredient] = useState([]);
  const [dbMinutes, setdbMinutes] = useState([]);
  const [dbTags, setdbTags] = useState([]);
  const [personName, setPersonName] = useState([]);
  const [ingredient, setingredient] = useState([]);
  const [minutes, setminutes] = useState("");
  const [tags, setTags] = useState([]);
  const [searchbar, setsearchbar] = useState("");
 
  
  const getRecipeByFilter = (e) => {
    e.preventDefault()
    try{
      console.log(
        {
          "ingredients": ingredient,
          "minutes" : minutes,
          "tags" : tags,
          "search": searchbar
        } 
      )
      axios.post("http://localhost:8000/recipe/filter", {
        "ingredients": ingredient,
        "minutes" : minutes,
        "tags" : tags,
        "search": searchbar
      }).then(
        (res) => {
          console.log(res)
        }
      )
    } catch (e) {

    }
  }

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setPersonName(
      // On autofill we get a stringified value.
      typeof value === "string" ? value.split(",") : value
    );
  };

  const handleChangeIngredient = (event) => {
    const {
      target: { value },
    } = event;
    setingredient(
      // On autofill we get a stringified value.
      typeof value === "string" ? value.split(",") : value
    );
  };

  const handleChangeMinutes = (event) => {
    const {
      target: { value },
    } = event;
    setminutes(value);
  };

  const handleChangeTags = (event) => {
    const {
      target: { value },
    } = event;
    setTags(value);
  };

  const onClickButton = () => {
    console.log(
      {
        "ingredients": ingredient,
        "minutes" : minutes,
        "tags" : tags,
        "search": searchbar
      }
    )
  };

  const handleSearchChange = (event) => {
    const {
      target: { value },
    } = event;
    setsearchbar(value);
  }


  return (
    <div>
      <Box
      sx={{
        pt: 5,
        pb: 2,
        mx: 40,
        textalign: 'center',
        width: 645,
        maxWidth: '100%',
      }}
    >
      <TextField 
      onChange={handleSearchChange} fullWidth label="Search" id="fullWiwkdth" />
    </Box>
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-multiple-chip-label">Ingredients</InputLabel>
        <Select
          labelId="demo-multiple-chip-label"
          id="demo-multiple-chip"
          multiple
          value={ingredient}
          onChange={handleChangeIngredient}
          input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
          renderValue={(selected) => (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          MenuProps={MenuProps}
        >
          {ingredientsArray.map((name) => (
            <MenuItem
              key={name}
              value={name}
              style={getStyles(name, personName, theme)}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id="demo-simple-select-helper-label">Minutes</InputLabel>
        <Select
          labelId="demo-simple-select-helper-label"
          id="demo-simple-select-helper"
          value={minutes}
          label="Age"
          onChange={handleChangeMinutes}
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          <MenuItem value={15}>less than 15 min</MenuItem>
          <MenuItem value={30}>30 min</MenuItem>
          <MenuItem value={45}>45 min</MenuItem>
          <MenuItem value={60}>60 min</MenuItem>
        </Select>
      </FormControl>
      <FormControl sx={{ m: 1, width: 190 }}>
        <InputLabel id="demo-multiple-chip-label">Tags</InputLabel>
        <Select
          labelId="demo-multiple-chip-label"
          id="demo-multiple-chip"
          multiple
          value={tags}
          onChange={handleChangeTags}
          input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
          renderValue={(selected) => (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          MenuProps={MenuProps}
        >
          {tagsArray.map((name) => (
            <MenuItem
              key={name}
              value={name}
              style={getStyles(name, personName, theme)}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <div class="p-5">
      <button
        onClick={getRecipeByFilter}
        class="mx-auto w-1/2 mt-5 rounded-full py-5 text-gray-900 bg-blue-200 border border-black-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-semi text-sm px-5 py-4 dark:bg-black dark:text-white dark:border-white-100 dark:hover:bg-gray-700 dark:hover:border-black-600 dark:focus:ring-gray-700"
      >
        Submit 
      </button>
      </div>
    </div>
  );
}
