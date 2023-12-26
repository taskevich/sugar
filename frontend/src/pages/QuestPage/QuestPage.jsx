import {useEffect, useState} from "react"
import {useParams} from "react-router-dom"
import {useNavigate} from "react-router";
import InfoBLock from "../../componets/InfoBlock/InfoBlock"
import PrevLegend from "../../componets/UI/PrevLegend/PrevLegend"
import GalleryQuest from "../../componets/UI/GalleryQuest/GalleryQuest"
import Review from "../../componets/UI/Review/Review"
import API from "../../API/Api";
import Sheduls from "../../componets/UI/Sheduls/Sheduls";
import "./style.scss"

const QuestPage = () => {
    const nav = useNavigate()
    const match = useParams()
    const slug = match.slug
    const [quest, setQuest] = useState([])
    const [load, setLoad] = useState(true)
    const [reviews, setReview] = useState([])

    useEffect(() => {

        const dataQuest = async () => {
            const data = await API.get(`/get_quest/${slug}`)

            if (data.data.payload === null) {
                nav("/");
            } else {
                setReview(data.data.payload.reviews)
                setQuest(data.data.payload.quest);
                setLoad(false);
            }
        }
        dataQuest()
    }, [slug, nav])


    if (load) {
        return (
            <div className="Loading">
                loading
            </div>
        )
    }

    return (
        <div className="questPage">
            <div className="wrapper">
                <p>Квест {quest.description}</p>
                <h1>{quest.name}</h1>
                <InfoBLock quest={quest}/>
                <PrevLegend quest={quest}/>
                <GalleryQuest id={quest.id}/>
                <Review reviews={reviews}/>
                <Sheduls id={quest.my_erp_id}/>
            </div>
        </div>

    )
}
export default QuestPage