import axios from 'axios';


export default class PostService {
    static async login(data) {
        return await axios.post(
            '/auth/jwt/login',
            data,
            {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                },
                withCredentials: true
            }
        ).catch ((e) => {return {
            error: e.message
        }});
    };

    static async register(data) {
        return await axios.post(
                '/auth/register',
                data,
                {
                    withCredentials: true
                }
            ).catch ((e) => {return {
            error: e.message
        }});
    };


    static async sendStrategy(data) {
        return await axios.post(
            '/strategy',
            data,
            {
                withCredentials: true
            }
        ).catch ((e) => {return {
            error: e.message
        }});
    }

    static async sendUserSettings(data) {
        return await axios.post(
            '/user/settings',
            data,
            {
                withCredentials: true
            }
        ).catch ((e) => {return {
            error: e.message
        }});
    }

}

