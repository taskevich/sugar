import React, {useEffect, useState} from "react";
import AliceCarousel from "react-alice-carousel";
import getAll from "../../../API/getAll";


const PhotoList = () => {
    const [image, setImage] = useState()
    const Fetch = async () => {
        const res = await getAll("/get_photos?is_main=true")
        setImage(res.payload)
    }

    useEffect(()=> {
        Fetch()
    }, [])
    const responsive= {
        1440: { items: 5, itemsFit: "contain"},
        1270: {items: 3, itemsFit: "contain"},
        1024: {items: 3, itemsFit: "contain"},
        990: {items: 3, itemsFit: "contain"},
        660: { items: 2, itemsFit: "contain"},
        480: {items: 1, itemsFit: "contain"},
        320: {items: 1, itemsFit: "contain"}
    }
    if(image === undefined) {
        return <></>
    }
    const items =
        image.map((img, index) => (

            <img src={`http://45.12.238.117:8000/get_image?image_path=/app/${Object.values(img)[0]}`} key={index} alt=""/>
        ))

    return (
        <>
            <AliceCarousel infinite={image.length >= 5} autoPlay={image.length >= 5} autoPlayInterval={5000} disableDotsControls={true} responsive={responsive} disableButtonsControls={true} items={items}/>
        </>
    )
}

export default PhotoList