import deff from "../../assets/DefaultImage.png"
import arrow from "../../assets/icon/ArrowLeft.svg"
import {useCallback, useEffect, useRef, useState} from "react"
import API from "../../API/Api"
import {useParams} from "react-router"
import {Link} from "react-router-dom";
import ImageQuestList from "./ImageQuestList";
import getAll from "../../API/getAll";
import Cookie from "js-cookie";
import ReviewBlock from "./ReviewBlock/ReviewBlock";

const UpdateQuest = () => {
    const match = useParams()
    const slug = match.slug
    const [page, setPage] = useState()
    const [image, setImage] = useState()
    const [quest, setQuest] = useState({
        name:"",
        slug:"",
        description: "",
        price:"",
        hard_id: "",
        horror_id:  "",
        legend: "",
        min_players: "",
        max_players: "",
        count_actors: "",
        play_time: "",
        age_limit: "",
        is_hide: "",
        my_erp_id: "",
    })


    const ref = useRef()

    const handleChange = (e) => {
        const {name, value} = e.target
        setQuest({...quest, [name]: value})
    }

    const toogleChange = (e) => {
        if (e.target.value === "false") {
            setQuest({...quest, is_hide: true})
        } else {
            setQuest({...quest, is_hide: false})
        }
    }

    const imageChange = (e) => {
        setPage(e.target.files[0])
    }

    const fetch = useCallback(async () => {
        try {
            const quest = await getAll(`/get_quest/${slug}`)
                setQuest(quest.payload.quest)
                const photo = Object.values(quest.payload.quest.files)
                setImage(photo[0])
        } catch (error) {
            console.log(`${error}`);
        }
    }, [slug])

    const addPhoto = async (id) => {
        try {
            const formData = new FormData()
            formData.append("file", page)
            const file = formData.get("file")
            await API.post(`admin/panel/set_photo?quest_id=${id}`, {
                file
            }, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })
            await fetch()

        }
        catch (error) {
            console.log(error)
        }
    }
    const handleSubmit = async () => {
        try {
            const response = await API.post(`/admin/panel/update/${quest.id}`, {
                name: quest.name,
                slug: quest.slug,
                description: quest.description,
                price: quest.price,
                hardId: quest.hard_id,
                horrorId: quest.horror_id,
                legend: quest.legend,
                minPlayers: quest.min_players,
                maxPlayers: quest.max_players,
                countActors: 1,
                playTime: quest.play_time,
                ageLimit: quest.age_limit,
                isHide: quest.is_hide,
                myErpId: quest.my_erp_id
            }, {
                headers: {
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })

            if (!response.data.error) {

                if (ref.current.value !== "") {
                    addPhoto(quest.id)
                }

                fetch()
            } else {
                alert("Невозможно обновить квест: " + response.data.message)
            }
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        fetch()
    }, [fetch])

    return (
        <>
            <div className="questAdmin">
                <Link className="arrow" to="/admin/panel"><img src={arrow} alt="imgjh"/></Link>
                <div className="block_1">
                    <div className="text">
                        <p>Название: <input name="name" value={quest.name} onChange={handleChange}/></p>
                        <p>MyErpId: <input name="my_erp_id" value={quest.my_erp_id} onChange={handleChange}/></p>
                        <p>Code название: <input name="slug" value={quest.slug} onChange={handleChange}/></p>
                        <p>Тип квеста: <input name="description" value={quest.description} onChange={handleChange}/></p>
                        <p>Цена: <input name="price" value={quest.price} onChange={handleChange}/></p>
                        <p>Минимум игроков: <input name="min_players" value={quest.min_players}
                                                   onChange={handleChange}/></p>
                        <p>Максимум игроков: <input name="max_players" value={quest.max_players}
                                                    onChange={handleChange}/></p>
                        <p>Уровень страха: <input name="horror_id" value={quest.horror_id} onChange={handleChange}/></p>
                        <p>Уровень сложности: <input name="hard_id" value={quest.hard_id} onChange={handleChange}/></p>
                        <p>Возрастное ограничение: <input name="age_limit" value={quest.age_limit}
                                                          onChange={handleChange}/></p>
                        <p>Игровое время: <input name="play_time" value={quest.play_time} onChange={handleChange}/></p>
                        <p>Скрыть: {quest.is_hide ? <span>true</span> : <span>false</span>} <input type="checkbox" name="is_hide"
                                                                                      value={quest.is_hide}
                                                                                      checked={quest.is_hide ? true : false}
                                                                                      onChange={toogleChange}/></p>
                    </div>
                    <div className="img">
                        {quest.files === null ? <img src={deff} alt=""/> : <img src={`http://45.12.238.117:8000/get_image?image_path=/app/${image}`} alt=""/>}
                        <input type="file" ref={ref} onChange={imageChange}/>
                    </div>
                </div>
                <div className="block_2">
                    <p>Легенда: </p>
                    <textarea name="legend" value={quest.legend} onChange={handleChange}/>
                    <button onClick={handleSubmit}>Изменить</button>
                </div>
            </div>
            <ImageQuestList id={quest.id}/>
            <ReviewBlock quest={quest.id}/>
        </>
    )
}
export default UpdateQuest