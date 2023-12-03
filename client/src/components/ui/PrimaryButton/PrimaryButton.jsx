import React from 'react';
import './PrimaryButton.scss';

const PrimaryButton = ({ action, children }) => {
    const handleClick = (event) => {
        event.preventDefault();
        action();
    };

    return (
        <button className="primary-button" onClick={handleClick}>
            {children}
        </button>
    );
};

export default PrimaryButton;