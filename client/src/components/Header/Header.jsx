import React, { useState } from 'react';
import avatarImage from '../../assets/logo.svg';
import './Header.scss';

const Header = ({ onSearch }) => {
    const [search, setSearch] = useState('');

    const handleSearchChange = (event) => {
        setSearch(event.target.value);
        onSearch(event.target.value);
    };

    return (
        <div className="header">
            <div className="avatar">
                <img className={"avatar"} src={avatarImage} alt="Avatar" />
            </div>
            <input
                type="text"
                className="search-bar"
                placeholder="Поиск..."
                value={search}
                onChange={handleSearchChange}
            />
        </div>
    );
};

export default Header;
