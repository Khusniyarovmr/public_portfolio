import React, {useState} from "react";
import Modal from "../../Components/Modal/Modal";
import Authenticate from "../Authenticate/Authenticate";
import {NavLink} from "react-router-dom";


const Navbar = () => {
    const [show, setShow] = useState(false);
    function handleChangeShowModal() {
        show === false?setShow(true):setShow(false);
    }


    return (
        <section>
            <nav>
                <ul>
                    <li>
                        <NavLink to="/home" style={{
                            fontVariant: "small-caps",
                            fontSize: "36px",
                            color: "#000000"
                        }}>CryptoTrade</NavLink>
                    </li>
                    <li>
                        {/*TODO: check user permissions*/}
                        <NavLink to="/dashboard">Dashboard</NavLink>
                    </li>
                    <li>
                        <button onClick={handleChangeShowModal}>Sign in</button>
                        <Modal title="Авторизация" onClose={() => setShow(false)} show={show}>
                            <Authenticate showModal={handleChangeShowModal}/>
                        </Modal>
                    </li>
                </ul>
            </nav>
        </section>
    )
}

export default Navbar;