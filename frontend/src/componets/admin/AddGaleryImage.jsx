import API from "../../API/Api";
import Cookie from "js-cookie";
import {useState} from "react";

const AddGaleryImage = ({update}) => {
    const [page, setPage] = useState()
    const addPhoto = async () => {
        try {
            const formData = new FormData()
            formData.append("file", page)
            const file = formData.get("file")
            const response = await API.post(`add_photo?is_main=true`, {
                file
            }, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })
            if (!response.data.error)
                update()
            else
                alert(response.data.message)
        }
        catch (error) {
            console.log(error)
        }
    }
    const handleImage = (e) => {
        setPage(e.target.files[0])
    }

    return(
        <div>
            <input type="file" onChange={handleImage}/>
            <button onClick={addPhoto}>Добавить фото</button>
        </div>
    )
};

export default AddGaleryImage;