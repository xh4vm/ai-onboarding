import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Импорт Link из react-router-dom
import logo from '../../assets/logo.svg';
import './NavigationMenu.scss';

const NavigationMenu = () => {
    const [activeMenuItem, setActiveMenuItem] = useState('');

    const handleMenuItemClick = (path) => {
        setActiveMenuItem(path);
        console.log(activeMenuItem);
    };

    return (
        <div className="navigation-menu">
            <img height={130} width={130} src={logo} alt="Logo" className="logo" />

            <Link to="/" className={`menu-item`} onClick={() => handleMenuItemClick('/')}>
                <span className={activeMenuItem === '/' ? 'active' : ''}>Главная</span>
            </Link>
            <Link to="/tasks" className={`menu-item`} onClick={() => handleMenuItemClick('/applications')}>
                <span className={activeMenuItem === '/tasks' ? 'active' : ''}>Задачи</span>
            </Link>
            <Link to="/support" className={`menu-item`} onClick={() => handleMenuItemClick('/support')}>
                <span className={activeMenuItem === '/support' ? 'active' : ''}>Поддержка</span>
            </Link>
            <Link to="/chat" className={`menu-item`} onClick={() => handleMenuItemClick('/chat')}>
                <span className={activeMenuItem === '/chat' ? 'active' : ''}>Чат</span>
            </Link>

            <div className="spacer"/>

            <Link to="/logout" className={`logout-text`} onClick={() => handleMenuItemClick('/logout')}>
                <span className={activeMenuItem === '/logout' ? 'active' : ''}>Выйти</span>
            </Link>
        </div>
    );
};

export default NavigationMenu;
