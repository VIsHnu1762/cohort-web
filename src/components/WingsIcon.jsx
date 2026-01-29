import React from 'react';

const WingsIcon = ({ size = 24 }) => {
  return (
    <span
      style={{
        fontSize: `${size}px`,
        lineHeight: 1,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      🪽
    </span>
  );
};

export default WingsIcon;
