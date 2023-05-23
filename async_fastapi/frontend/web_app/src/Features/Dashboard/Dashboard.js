import React from "react";
import DashboardNavBar from "./dashboardNavbar";
import DashboardRouter from "./dashboardRouter";

const Dashboard = () => {
    return (
        <div className="dashboard">
            <DashboardNavBar/>
            <DashboardRouter/>
        </div>
    )
};

export default Dashboard;