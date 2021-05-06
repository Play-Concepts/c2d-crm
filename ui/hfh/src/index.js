import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter } from 'react-router-dom';
import './index.css';
import './assets/fomantic/dist/semantic.css';
import * as serviceWorker from './serviceWorker';
import MainPage from "./pages/main";

const rootElement = document.getElementById('root');

const renderApp = Component => {
    ReactDOM.render(
        <HashRouter>
            <Component/>
        </HashRouter>,
        rootElement
    );
};

renderApp(MainPage);
if (module.hot) {
    module.hot.accept('./pages/main', () => {
        const NextApp = require('./pages/main').default;
        renderApp(NextApp);
    });
}
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();