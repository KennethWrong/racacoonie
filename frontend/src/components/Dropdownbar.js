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

const names = [
  "Oliver Hansen",
  "Van Henry",
  "April Tucker",
  "Ralph Hubbard",
  "Omar Alexander",
  "Carlos Abbott",
  "Miriam Wagner",
  "Bradley Wilkerson",
  "Virginia Andrews",
  "Kelly Snyder",
];

const ingredientsArray = ["Apple", "Onion", "Grapes", "Tea"];

const tagsArray = ["Italian", "French", "Easy", "Boy"];

const minutesArray = ["5 minutes", "10 minutes", "15 minutes", "30 minutes"];

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

  useEffect(() => {
    fetch()
      .then((resp) => {
        resp.json()
      })
      .then((resp) => {
        setdbIngredient(resp.ingredients);
        setdbMinutes(resp.minutes);
        setdbTags(resp.tags);
      });
  }, []);

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

  const handleButtonChange = () => {
    console.log(personName);
  };

  return (
    <div>
      <FormControl sx={{ m: 1, width: 190 }}>
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
          <MenuItem value={10}>Ten</MenuItem>
          <MenuItem value={20}>Twenty</MenuItem>
          <MenuItem value={30}>Thirty</MenuItem>
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
      <button
        onClick={handleButtonChange}
        class="mt-4 text-gray-900 bg-blue-200 border border-black-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-semi text-sm px-5 py-2.5 mr-2 mb-2 mx-auto dark:bg-black dark:text-white dark:border-white-100 dark:hover:bg-gray-700 dark:hover:border-black-600 dark:focus:ring-gray-700"
      >
        Submit
      </button>
    </div>
  );
}
