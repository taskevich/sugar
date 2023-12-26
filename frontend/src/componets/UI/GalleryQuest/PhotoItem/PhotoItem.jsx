const PhotoItem = ({img}) => {
    const photos = Object.values(img)
    return (
        // <div className="photoItem">
            <img src={photos} alt="" />
        // </div>
    )
}

export default PhotoItem