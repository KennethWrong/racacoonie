import React from 'react';
import { ErrorMessage } from '@hookform/error-message';

const Input = React.forwardRef((props, ref) => (
  <div className={'px-3 ' + props.className}>
    {props.label ? (
      <label
        className='form-label block text-gray-800 text-sm font-medium mb-1'
        htmlFor={props.name}
      >
        {props.label}
        {props.required ? <span className='text-red-600'>*</span> : null}
      </label>
    ) : null}

    <input
      className='form-input w-full text-gray-800 outline-none'
      name={props.name}
      type={props.type ? props.type : 'text'}
      placeholder={props.placeholder}
      ref={ref}
      maxLength={props.maxLength}
      onChange={(event) =>
        props.onChangeText ? props.onChangeText(event.target.value) : ''}
    />
    {props.errors ? (
      <p className='block text-sm font-medium text-red-600'>
        <ErrorMessage errors={props.errors} name={props.name} />
      </p>
    ) : null}
  </div>
));

export default Input;
