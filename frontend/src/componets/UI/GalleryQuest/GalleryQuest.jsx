import {useCallback, useEffect, useState} from "react";
import API from "../../../API/Api";
import "./style.scss"
import AliceCarousel from "react-alice-carousel";

const GalleryQuest = ({id}) => {
    const [image, setImages] = useState([])
    const Fetch = useCallback(async (id) => {
        const page = await API.get(`/get_photos?quest_id=${id}`)
        setImages(page.data.payload)
    }, [])

    useEffect(() => {
        console.log("ok")
        if (id === undefined) {

        } else {
            Fetch(id)
        }
        if (image === undefined) {
            Fetch(id)
        }
    }, [Fetch, id])

    if (image.length === 0) {
        return (
            <></>
        )
    }
    const responsive = {
        1440: { items: 2, itemsFit: "contain"},
        1270: {items: 2, itemsFit: "contain"},
        1024: {items: 2, itemsFit: "contain"},
        800: { items: 2, itemsFit: "contain"},
        480: {items: 1, itemsFit: "contain"},
        320: {items: 1, itemsFit: "fill"}
    }
    const itemsImage =
        image.map((img, index) => (
            <img src={`http://45.12.238.117:8000/get_image?image_path=/app/${Object.values(img)[0]}`} key={index} alt=""/>
        ))

    return (
        <div className="gallery">
            <h1>Фотогалерея</h1>
            <AliceCarousel items={itemsImage} responsive={responsive} disableButtonsControls={true} disableDotsControls={true} autoPlay={image.length > 2} autoPlayInterval={3000} infinite={true} />
        </div>
    )
}

export default GalleryQuest;