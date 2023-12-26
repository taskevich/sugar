import React, {useCallback, useEffect, useState} from 'react';
import API from "../../../API/Api";
import Cookie from "js-cookie";
import AddReview from "./AddReview/AddReview";
import "./style.scss"

const ReviewBlock = ({quest})=> {
    const [reviews, setReviews] = useState([])

    const DeleteReview = async (id) => {
        try {
            await API.delete(`/admin/reviews/delete/${id}`, {
                headers: {
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })
            alert("Отзыв удален")
            Fetch()
        }
        catch (error) {
            console.log(error)
        }
    }
    const Fetch = useCallback(async () => {
        try {
            const res = await API.post(`/admin/get_reviews?quest_id=${quest}`, {},{
                headers: {
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })
            setReviews(res.data.payload)
        }
        catch (error) {
            console.log(error)
        }
    }, [quest])


    useEffect(() => {
        if (quest > 0) {
            Fetch()
        }
    }, [Fetch, quest])

    if(reviews.length === 0) {
        return <h1>Нету отзывов</h1>
    }

    return (
        <div className="reviews">
            <div className="reviewList">
                {reviews.map((review) => (
                    <div className="review">
                        <h1>{review.visitor}</h1>
                        <p>{review.message}</p>
                        <p>Звезд: {review.stars}</p>
                        <button onClick={() => DeleteReview(review.id)}>Удалить отзыв</button>
                    </div>
                ))}
            </div>

            <AddReview quest={quest} Fetch={Fetch}/>
        </div>
    )
};

export default ReviewBlock;