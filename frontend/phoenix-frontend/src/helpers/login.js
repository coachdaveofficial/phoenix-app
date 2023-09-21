import axios from "axios";
const LOGIN_URL = 'http://127.0.0.1:8080/auth/login/';

export default async function login(data) {
    let response;
    try {
        response = await axios.post(`${LOGIN_URL}`, data, {withCredentials: true});
    } catch (e) {
        response = e;
    }

    return response;
}