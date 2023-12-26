import {Link} from "react-router-dom"
import deff from "../../assets/DefaultImage.png";
import getAll from "../../API/getAll";
import {useEffect, useState} from "react";

const QuestAdmin = ({quest, removeQuest}) => {
    const [image, setImage] = useState()
    useEffect(() => {
        if (quest.files !== null) {
            const photo = Object.values(quest.files)
            setImage(photo)
        }
    }, [])
    return (
        <>
            <Link className="questLink" to={`/admin/panel/update/${quest.slug}`}>
                <h1>{quest.name}</h1>
                {quest.files === null  ? <img src={deff} alt=""/> : <img src={`http://45.12.238.117:8000/get_image?image_path=/app/${image}`} alt=""/>}
            </Link>
            <button onClick={() => removeQuest(quest.id)}>Удалить квест</button>

        </>
    )
}
export default QuestAdmin