import React from "react";
import API from "../../../API/Api";
import Cookie from "js-cookie";


const GalleryItem = ({item, update}) => {
    const photos = Object.values(item)
    const id = Number(Object.keys(item).toString())
    const deletePhoto =  async () => {
        try {
            await API.delete(`/admin/remove_photo/${id}`, {
                headers: {
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })
            await update()
        }
        catch (error) {
            sessionStorage.setItem("auth", false)
            Cookie.set("access_token_cookie", "")
        }
    }
    return(
        <>
            <div className="questItem">
                <img  src={`http://45.12.238.117:8000/get_image?image_path=/app/${photos[0]}`} alt=""/>
                <button onClick={deletePhoto}>Удалить</button>
            </div>
        </>
    )
};

export default GalleryItem;