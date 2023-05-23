import React, {useEffect} from 'react';
import Navbar from "./Features/Navbar/Navbar";
import AppRouter from "./Routes/AppRouter";
import FetchService from './API/GetService';


function App() {

    useEffect(() => {
        FetchService.getCSRFToken();
    }, []);


    return (

        <div>
            <header>
                <Navbar/>
            </header>
            <AppRouter/>
        </div>

    );
}

export default App;
