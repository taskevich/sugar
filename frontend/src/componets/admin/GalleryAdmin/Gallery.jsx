import React from 'react';
import GalleryItem from "./GalleryItem";

const Gallery = ({imagesList, update}) => {


    if (imagesList === undefined) {
        return <></>
    }
    return (
        <div className="gallery_quest">
            {imagesList.map((item, index) => (
                <GalleryItem item={item} update={update} key={index}/>
            ))}
        </div>
    )
}

export default Gallery;