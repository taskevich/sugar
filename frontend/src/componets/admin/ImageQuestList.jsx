import ImageItem from "./ImageItem";
import {useCallback, useEffect, useState} from "react";
import API from "../../API/Api";
import Cookie from "js-cookie";
import {useNavigate} from "react-router";
import getAll from "../../API/getAll";

const ImageQuestList = ({id}) => {
    const nav = useNavigate()
    const [image, setImage] = useState();
    const [page, setPages] = useState("");

    const addPhotos = async () => {
        try {
            const formData = new FormData()
            formData.append("file", page)
            const file = formData.get("file")
            await API.post(`/add_photo?quest_id=${id}`, {
                file
            }, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })
            Fetch(id)
        }
        catch (error) {
            console.log(error)
        }
    }

    const onChange = (e) => {
        setPages(e.target.files[0])
    }

    const Fetch = useCallback(async (id) => {
        try {
            const page = await getAll(`/get_photos?quest_id=${id}`)
            setImage(page?.payload)
        }
        catch (error) {
            console.log(error.message)
        }
    }, [])

    useEffect(() => {
            Fetch(id)
    }, [Fetch, id])

    return (
        <>
            <div className="AdminImages">
                {
                    image !== undefined ? <>{
                        image.map((img, index) => (
                            <ImageItem fetch={Fetch} id_quest={id} key={index} img={img}/>
                        ))
                    }</> : <></>
                }

            </div>
            <input type="file" onChange={onChange}/>
            <button className="btnAdd" onClick={addPhotos}>Добавить</button>
        </>
    )
};

export default ImageQuestList;