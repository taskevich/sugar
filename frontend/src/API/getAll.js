
import API from "./Api";
import Cookie from "js-cookie";

const getAll = async (url) => {
    try {
        const res = await API.get(url, {
            headers: {
                Authorization: `Bearer ${Cookie.get("access_token_cookie")}`
            }
        })
        return res.data
    }
    catch (error) {
        console.log(error)
    }
}

export default getAll