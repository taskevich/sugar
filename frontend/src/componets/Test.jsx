import React from 'react';
import AliceCarousel from "react-alice-carousel";
import deff from "./../assets/DefaultImage.png"
import test from "./../assets/image 4.png"
const Test = (props) => {
    const responsive = {
        1440: { items: 5, itemsFit: "contain"},
        1270: {items: 3, itemsFit: "contain"},
        1024: {items: 2, itemsFit: "contain"},
        660: { items: 2, itemsFit: "contain"},
        480: {items: 1, itemsFit: "contain"},
        320: {items: 1, itemsFit: "contain"}
    }
    const items = [
        <img src={test} alt=""/>,
        <img src={deff} alt=""/>,
        <img src={deff} alt=""/>,
        <img src={deff} alt=""/>,
        <img src={deff} alt=""/>,
        <img src={deff} alt=""/>,
    ]

    return (
        <>
            <AliceCarousel  infinite={true} disableDotsControls={true} responsive={responsive} disableButtonsControls={true}  items={items}/>
        </>
    )
};

export default Test;