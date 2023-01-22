import React from 'react';

const StatusLabel = (props) => {
  const bgColors = {
    delay: 'rgba(242, 19, 93, 0.2)',
    processing: 'rgba(255, 130, 0, 0.2)',
    reanalyzing: 'rgba(17, 0, 255, 0.11)',
    pending: 'rgba(17, 0, 255, 0.11)',
    ready: 'rgba(23, 201, 100, 0.2)',
    none: 'rgba(75, 81, 93, 0.3)'
  };

  const textColors = {
    delay: '#CC0000', // danger
    processing: '#FF8800', // warning
    reanalyzing: '#aa66cc',
    pending: '#aa66cc', // secondary
    ready: '#00C851', // success
    none: '#3E4551' // grey
  };

  return (
    // rounded-full mb-0 text-center align-middle text-bold-500
    <div
      className='item-bubble'
      style={{
        height: 'auto',
        minWidth: '50%',
        padding: '5px 15px',
        borderRadius: '500px',
        color: textColors[props.status],
        backgroundColor: bgColors[props.status],
        ...props.style
      }}
    >
      <span className='capitalize text-sm'>{props.text ? props.text : props.status}</span>
    </div>
  );
};

export default StatusLabel;
