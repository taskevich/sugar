import React from 'react';
import API from "../../API/Api";
import Cookie from "js-cookie";
import {useNavigate} from "react-router";

const ImageItem = ({img , fetch, id_quest}) => {

    const nav = useNavigate()
    const photos = Object.values(img)
    const id = Number(Object.keys(img).toString())

    const deletePhoto =  async () => {
        try {
            await API.delete(`/admin/remove_photo/${id}`, {
                headers: {
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })
            await fetch(id_quest)
        }
        catch (error) {
            sessionStorage.setItem("auth", false)
            Cookie.set("access_token_cookie", "")
            nav("/admin")
        }

    }

    return (
        <div className="imagePhoto">
            <img  src={`http://45.12.238.117:8000/get_image?image_path=/app/${photos[0]}`} alt=""/>
            <button onClick={deletePhoto}>Удалить</button>
        </div>

    );
}

export default ImageItem;