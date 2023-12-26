import axios from "axios";
import Cookie from "js-cookie";
const url = "http://45.12.238.117:8000/"

const API = axios.create({
    baseURL: url,
    
    headers: {
        Authorization: `Bearer ${Cookie.get("access_token_cookie")}`
    }
})


export default API;