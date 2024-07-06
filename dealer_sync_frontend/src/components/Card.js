import React from 'react';

const Card = ({ children, className }) => {
  return (
    <div className={`bg-background-light shadow-md rounded-lg p-6 transition-shadow duration-300 hover:shadow-lg ${className}`}>
      {children}
    </div>
  );
};

export default Card;
