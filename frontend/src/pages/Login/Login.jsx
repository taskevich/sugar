import {useEffect, useState} from "react";
import {useNavigate} from "react-router";
import Api from "../../API/Api";
import Cookie from "js-cookie";


const Login = () => {
    const nav = useNavigate()
    const [logData, setLogData] = useState({
        username: "",
        password: ""
    })

    const  handleChange = (e) => {
        const {name, value} = e.target
        setLogData({
            ...logData,
            [name]: value
        })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const log = await Api.post("admin/login", logData)
            if (!log.data.error) {
                sessionStorage.setItem("auth", true)
                Cookie.set("access_token_cookie", log.data.payload)
                nav("panel")
            } else {
                alert(log.data.message)
            }
        }
        catch (error) {
            console.log(error)
        }
    }
    useEffect(() => {
        if (sessionStorage.getItem("auth") === "true") {
            console.log(true)
            nav("panel")
        }
    }, [nav]);
    return(
        <div className="admin_window">
            <div className="admin_login">
            <h1>ВХОД</h1>
                <form onSubmit={handleSubmit}>
                    <p>Login</p>
                    <input type="text" name="username" value={logData.username} onChange={handleChange} />
                    <p>Password</p>
                    <input type="password" name="password" value={logData.password} onChange={handleChange} />
                    <button type="submit">Зайти</button>
                </form>
            </div>
        </div>
    )
};

export default Login;
