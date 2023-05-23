import React, {useState} from 'react'
import PostService from "../../../API/PostService";
import toast, { Toaster } from 'react-hot-toast';
import serializeForm from "../../../Utils/formSerializer";


export default function Registration(props) {

    const [pwd, setPwd] = useState('');
    function handleChangePwd(e) {
        setPwd(e.target.value);
    }

    async function sendAuthData(event) {
        event.preventDefault();
        let data = serializeForm(event.target);
        let { status, error } = await PostService.register(data);

        if (status === 201) {
            onSuccess();
        } else {
            onError(error);
        }
    }

    function onSuccess() {
        toast('Регистрация прошла успешно!');
        setTimeout(props.showModal, 2500);
    }

    function onError(e) {
        toast(`Не удалось зарегистрироваться ${e}`);
    }

    return (
        <>
            <Toaster/>
            <form onSubmit={sendAuthData} action="" method="POST">
                <label>
                    <p>Username</p>
                    <input type="text"
                           placeholder="Введите имя пользователя"
                           autoComplete='new-password'
                           id="username"
                           name='username'/>
                </label>
                <label>
                    <p>Email</p>
                    <input type="email"
                           pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"
                           autoComplete='new-password'
                           placeholder="Введите email"
                           required
                           id="email"
                           name='email'/>
                </label>
                <label>
                    <p>Password</p>
                    <input type="password"
                           placeholder="Введите пароль"
                           title="Пароль должен содержать не менее 6 символов, включая ПРОПИСНЫЕ\строчные латинские буквы и цифры"
                           pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}"
                           required
                           autoComplete='new-password'
                           id="password"
                           name='password'
                           onChange={handleChangePwd}/>
                </label>
                <label>
                    <p>Confirm password</p>
                    <input type="password"
                           autoComplete='new-password'
                           pattern={pwd}
                           placeholder="Повторите пароль"
                           title="Пожалуйста, укажите пароль введенный выше!"
                           required/>
                </label><br/><br/>
                <button type="submit">Submit</button>
            </form>
            <p>Already have account? <button onClick={props.changeType}>Sign in</button></p>
            <p>Forgot your password? <span>Reset</span></p>
        </>
    )
}