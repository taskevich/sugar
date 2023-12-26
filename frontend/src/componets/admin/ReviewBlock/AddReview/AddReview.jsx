import {useState} from "react"
import API from "../../../../API/Api"
import Cookie from "js-cookie";
import "./style.scss"

const AddQuest = ({quest, Fetch}) => {
    const [review, setReview] = useState({
        name: '',
        message: '',
        stars: 1,
        questId: quest,
    })

    const update = () => {
        setReview({
            name: '',
            message: '',
            stars: '',
            questId: '',
        })
        Fetch()
    }
    const handleChange = (e) => {
        const {name, value} = e.target
        setReview({...review, [name]: value})
    }
    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const fetch = await API.post('/admin/reviews/add', {
                visitor: review.name,
                message: review.message,
                stars: Number(review.stars),
                questId: quest
            }, {
                headers: {
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })

            if (!fetch.data.error) {
                alert("Отзыв создан")
                update()
            } else {
                alert("Невозможно создать отзыв: " + fetch.data.message)
            }

        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div className="reviewAdd">
            <form className="form" onSubmit={handleSubmit}>
                <p>Имя посетителя</p>
                <input type="text" name='name' value={review.name} onChange={handleChange}/>
                <p>Текст отзыва</p>
                <input type="text" name='message' value={review.message} onChange={handleChange}/>
                <p>Количество звезд</p>
                <select name="stars" defaultValue={1} onChange={handleChange}>
                    <option value={1}>1</option>
                    <option value={2}>2</option>
                    <option value={3}>3</option>
                    <option value={4}>4</option>
                    <option value={5}>5</option>
                </select>
                <button>Добавить отзыв</button>
            </form>
        </div>
    )
}
export default AddQuest