import React from "react";
import logo from "../assets/images/logo.png";
import {ROOT_URL} from "../services/constants";
export const Header = props => {
    const handleLogoClick = () => window.location.href = ROOT_URL;

    const goHome = () => window.location.href = '/#/pages/start';

    return (
        <div>
            Put your header here.
            <img src={logo} alt="logo" onClick={handleLogoClick} />
        </div>
    );
};
