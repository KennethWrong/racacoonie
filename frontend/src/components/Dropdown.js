import React, { useEffect, useState } from 'react';
import './Dropdown.css';
import StatusLabel from './StatusLabel';

const Dropdown = (props) => {
  // const [selected, setSelected] = useState([]);

  // const [shownItems, setShownItems] = useState(props.items);

  // useEffect(() => {
  //   console.log(selected);
  // }, [selected]);

  const handleChange = (e) => {
    const selectedIds = Array.from(e.target.selectedOptions, option => option.value);
    const newSelected = props.items.filter(item => selectedIds.includes(item.id + ''));
    props.setState(newSelected);
  };

  return (
    <div className={props.className}>
      <div className='item-bubble-container'>
        <p>{props.name}</p>
        {props.selected.map((item) => (
          // <p key={item.id} className='item-bubble'>{item.name}</p>
          <StatusLabel key={item.id} text={item.name} status='reanalyzing' />
        ))}
      </div>

      <select onChange={handleChange} multiple>
        <option value='' disabled defaultValue>
          Select your {props.name}
        </option>
        {props.items.map((item) => (
          <option key={item.id} value={item.id}>{item.name}</option>
        ))}
      </select>
    </div>

  );
};

export default Dropdown;
