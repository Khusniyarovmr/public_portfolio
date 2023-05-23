import React from 'react';
import {Route, Routes} from 'react-router-dom';
import DashboardStatistic from "./Pages/Statistic";
import DashboardTrading from "./Pages/Trading";
import DashboardAnalytic from "./Pages/Analytic";
import DashboardSetting from "./Pages/Setting";


const DashboardRouter = () => {
    return (
        <Routes>
            <Route path='/statistic' element={<DashboardStatistic/>} key='dashboard/statistic'/>
            <Route path='/trading' element={<DashboardTrading/>} key='dashboard/trading'/>
            <Route path='/analytic' element={<DashboardAnalytic/>} key='dashboard/analytic'/>
            <Route path='/setting' element={<DashboardSetting/>} key='dashboard/setting'/>
        </Routes>
    );
};

export default DashboardRouter;