import React, { useEffect, useState } from 'react';
import { getAllTags } from '../api/api.js';
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

const TagsDropdown = (props) => {
  const theme = useTheme();

  const [tags, setTags] = useState([]);
  useEffect(() => {
    getAllTags().then((res) => {
      setTags(res.data.tags);
      console.log(res.data.tags);
    }).catch(e => { console.log(e); });
  }, []);

  return (
    <FormControl sx={{ m: 1, width: 190 }}>
      <InputLabel id='demo-multiple-chip-label'>Tags</InputLabel>
      <Select
        labelId='demo-multiple-chip-label'
        id='demo-multiple-chip'
        multiple
        value={props.selectedTags}
        onChange={props.handleChangeTags}
        input={<OutlinedInput id='select-multiple-chip' label='Chip' />}
        renderValue={(selected) => (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
            {selected.map((value) => (
              <Chip key={value} label={value} />
            ))}
          </Box>
        )}
        MenuProps={MenuProps}
      >
        {tags.map((tag) => (
          <MenuItem
            key={tag.id}
            value={tag.id}
            style={getStyles(theme)}
          >
            {tag.name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  // <div className='w-full px-3 mb-8'>
  //   <label
  //     className='form-label block text-gray-800 text-sm font-medium mb-1'
  //     htmlFor='tags'
  //   >
  //     Tags<span className='text-red-600'>*</span>
  //   </label>
  //   <select
  //     // ref={props.register}
  //     name='tags'
  //     className='form-select w-full focus:outline-none'
  //   >
  //     <option value='' disabled defaultValue>
  //       Select your Tags
  //     </option>

  //     {tags ? tags.map((tag) => (
  //       <option key={tag.id} value={tag.id}>{tag.name}</option>
  //     )) : null}

  //   </select>
  //   {/* <p className='block text-sm font-medium text-red-600'>
  //     <ErrorMessage errors={props.errors} name='category' />
  //   </p> */}
  // </div>
  );
};

export default TagsDropdown;
