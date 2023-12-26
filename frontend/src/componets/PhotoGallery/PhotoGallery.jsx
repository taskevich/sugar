import PhotoList from "./PhotoList/PhotoList"
import "./style.scss"


const PhotoGallery = () => {
    return (
        <div className="photoGallery">
            <div className="wrapper">
                <h1>Фотогалерея</h1>
                <PhotoList/>
            </div>
        </div>
    )
}

export default PhotoGallery