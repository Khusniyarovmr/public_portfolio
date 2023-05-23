import React from "react";
import serializeForm from "../../../Utils/formSerializer";
import PostService from "../../../API/PostService";
import toast, {Toaster} from "react-hot-toast";


export default function DashboardSetting() {

    async function handleSubmit(event) {
        event.preventDefault();
        const data = serializeForm(event.target);

        let {status, error} = await PostService.sendUserSettings(data);

        if (status === 200) {
            onSuccess();
        } else {
            onError(error, 'Вы не авторизованы!');
        }
    }
    function onSuccess() {
        toast('Успешно отправлено!');
    }

    function onError(e, msg) {
        toast(`${msg} ${e}`);
    }

    return (
        <>
            <Toaster/>
            <form onSubmit={handleSubmit} action="">
                <label>Market
                <input type="text" id="stock_market" name="stock_market"/>
                </label><br/>
                <label>Binance Key
                <input type="text" id="binance_key" name="binance_key"/>
                </label><br/>
                <label>Binance Secret
                <input type="text" id="binance_secret" name="binance_secret"/>
                </label><br/><br/>
                <input type="submit"/>
            </form>
        </>
    )
}

