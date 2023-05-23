import axios from 'axios';


export default class FetchService {
    static async getCSRFToken() {
        return await axios.get(
            '/form'
        ).catch ((e) => {return {
            error: e.message
        }});
    };

    static async getUserInfo() {
        return await axios.get(
            '/users/me'
        ).catch ((e) => {return {
            error: e.message
        }});
    }
}
