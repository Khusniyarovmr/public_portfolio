import React from 'react';
import {Route, Routes} from 'react-router-dom';
import Home from "../Features/Home/Home";
import Dashboard from "../Features/Dashboard/Dashboard";


const AppRouter = () => {
    return (
        <Routes>
            <Route path='/' element={<Home/>} exact={true} key='home'/>
                <Route path='home' element={<Home/>} exact={true} key='home'/>
                <Route path='dashboard/*' element={<Dashboard/>} key='dashboard'/>
        </Routes>
    );
};

export default AppRouter;