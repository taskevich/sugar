import React, {useEffect, useState} from 'react';
import getAll from "../../../API/getAll";
import Gallery from "../GalleryAdmin/Gallery";
import AddGaleryImage from "../AddGaleryImage";

const GalleryPage = () => {
    const [images, setImages] = useState()
    const Fetch = async () => {
        const res = await getAll("/get_photos?is_main=true")
        setImages(res.payload)
    }
    useEffect(() => {
        Fetch()
    }, []);
    return (
        <>
            <Gallery imagesList={images} update={Fetch}/>
            <AddGaleryImage update={Fetch}/>
        </>
    )
};

export default GalleryPage;