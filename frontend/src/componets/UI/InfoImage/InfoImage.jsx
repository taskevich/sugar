import deff from "../../../assets/DefaultImage.png"
import "./style.scss"

const InfoImage = ({quest}) => {
    return (
        <div className="infoImage">
            {quest.files === null ? <img src={deff} alt="" />: <img src={`http://45.12.238.117:8000/get_image?image_path=/app/${Object.values(quest.files)[0]}`} alt=""/> }
            
        </div>
    )
}

export default InfoImage