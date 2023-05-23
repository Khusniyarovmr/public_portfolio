import React, {useState} from "react";
import Login from "./Login/Login";
import Registration from "./Registration/Registration";


export default function Authenticate(props) {
    const [authType, setAuthType] = useState('login')

    if (authType === 'registration') {
        return (
            <>
                <Registration type={authType}
                              changeType={() => setAuthType('login')}
                              showModal={props.showModal}
                />
            </>
        )
    }

    return (
        <>
            <Login type={authType}
                   changeType={() => setAuthType('registration')}
                   showModal={props.showModal}
            />
        </>
    )
}