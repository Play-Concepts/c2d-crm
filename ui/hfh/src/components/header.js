import React from "react";
import {Menu, Image, Icon} from "semantic-ui-react";
import logo from "../assets/images/logo.png";
import {ROOT_URL} from "../services/constants";
export const Header = props => {
    const handleLogoClick = () => window.location.href = ROOT_URL;

    const doLogout = () => window.location.href = '/#/pages/logout';

    return (
        <Menu attached={'top'} inverted>
            <Menu.Item>
                <Image size={'small'} src={logo} onClick={handleLogoClick}/>
            </Menu.Item>
            <Menu.Menu position={'right'}>
                <Menu.Item>
                    <Icon name={'user'} size={'large'} onClick={doLogout}/>
                </Menu.Item>
            </Menu.Menu>
        </Menu>
    );
};
