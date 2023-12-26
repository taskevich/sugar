import Raiting from "./Raiting/Raiting"
import AliceCarousel from "react-alice-carousel";
import "./style.scss"

const Review = ({reviews}) => {


    if (reviews == null || reviews.length === 0) {
        return (
            <div></div>
        )
    }
    const responsive= {
        1440: { items: 3, itemsFit: "contain"},
        1270: {items: 3, itemsFit: "contain"},
        1024: {items: 3, itemsFit: "contain"},
        990: {items: 2, itemsFit: "contain"},
        690: { items: 2, itemsFit: "contain"},
        480: {items: 1, itemsFit: "contain"},
        320: {items: 1, itemsFit: "contain"}
    }

    const items = reviews.map((review) => (
            <div key={review.id} className="reviewItem">
                <div className="header">
                    <div className="title">
                        <p>{review.visitor}</p>
                    </div>
                    <Raiting raite={Number(review.stars)}/>
                </div>
                <div className="body">
                    <p>
                        {review.message}
                    </p>
                </div>
            </div>
        ))
    return (
        <div className="review">
            <h1>Отзывы</h1>

                <AliceCarousel items={items} autoPlayInterval={5000} infinite={reviews.length >= 3} autoPlay={reviews.length >= 3} disableDotsControls={true} responsive={responsive} disableButtonsControls={true}/>
        </div>
    )
}

export default Review