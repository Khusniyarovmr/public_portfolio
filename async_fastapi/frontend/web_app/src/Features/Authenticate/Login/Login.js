import React from 'react';
import PostService from '../../../API/PostService';
import toast, {Toaster} from 'react-hot-toast';
import serializeForm from "../../../Utils/formSerializer";
import FetchService from "../../../API/GetService";
import {useDispatch} from "react-redux";
import {setUserInfo} from "../../../Redux/Reducers/userSlice";

export default function Login(props) {
    const dispatch = useDispatch();

    async function sendAuthData(event) {
        event.preventDefault();
        let data = serializeForm(event.target);
        Object.defineProperty(data, 'username', Object.getOwnPropertyDescriptor(data, 'email'));
        delete data['email'];
        let {status, error} = await PostService.login(data);

        if (status === 200) {
            onSuccess();
            await AddUserInfo();
        } else {
            onError(error, 'Не удалось авторизоваться!');
        }
    }

    function onSuccess() {
        toast('Успешная авторизация!');
        setTimeout(props.showModal, 1000);
    }

    function onError(e, msg) {
        toast(`${msg} ${e}`);
    }

    async function AddUserInfo() {
        let {data, status, error}= await FetchService.getUserInfo();

        if (status === 200){
            const newUserData = {
                username: data.username,
                email: data.email,
                role_id: data.role_id,
                is_superuser: data.is_superuser,
                first_name: data.first_name,
                last_name: data.last_name,
                telegram_chat_id: data.telegram_chat_id,
            }

            if (newUserData){
                dispatch(
                    setUserInfo(newUserData)
                )
            }
        } else {
            onError(error, 'Не удалось получить данные пользователя')
        }

    }


    return (
        <>
            <Toaster/>
            <form onSubmit={sendAuthData} action="">
                <label>
                    <p>Email</p>
                    <input type="text"
                           pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"
                           autoComplete="EMAIL_ADDRESS"
                           placeholder="Введите email"
                           id='email'
                           name='email'
                           required/>
                </label>
                <label>
                    <p>Password</p>
                    <input type="password"
                           title="Пароль должен содержать не менее 6 символов, включая ПРОПИСНЫЕ\строчные латинские буквы и цифры"
                           pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}"
                           autoComplete="current-password"
                           placeholder="Введите пароль"
                           id="password"
                           name="password"
                           required/>
                </label><br/><br/>
                <button type="submit">Submit</button>
            </form>
            <p>Dont have account? <button onClick={props.changeType}>Sign up</button></p>
            <p>Forgot your password? <span>Reset</span></p>
        </>
    )
};