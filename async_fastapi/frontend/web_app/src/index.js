import React from 'react';
import App from './App';
import './Styles/inAppStyle.css';
import {createRoot} from 'react-dom/client';
import {Provider} from 'react-redux';
import {store} from './Redux/Redux-store';
import {BrowserRouter} from "react-router-dom";


const container = document.getElementById('root');
const root = createRoot(container);
root.render(
    <BrowserRouter>
        <Provider store={store}>
            <App/>
        </Provider>
    </BrowserRouter>
);
