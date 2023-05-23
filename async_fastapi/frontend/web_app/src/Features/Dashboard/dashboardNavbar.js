import React from 'react';
import {NavLink} from "react-router-dom";


export default function DashboardNavBar() {
    return (
        <div>
            <nav className="dashboardNav">
                <ul>
                    <li>
                        <NavLink to="statistic">
                            Statistics
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="trading">
                            Trading
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="analytic">
                            Analitics
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="setting">
                            Settings
                        </NavLink>
                    </li>
                </ul>
            </nav>
        </div>
    )
}

