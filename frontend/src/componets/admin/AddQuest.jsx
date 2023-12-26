import {useState, useRef} from "react"
import API from "../../API/Api"
import Cookie from "js-cookie";

const AddQuest = ({questData}) => {
    const [id_quest, setIDQuest] = useState()
    const [page, setPage] = useState()
    const [quest, setQuest] = useState({
        name: '',
        slug: '',
        desc: '',
        price: '',
        hard: 1,
        horror: 1,
        legend: '',
        min: '',
        max: '',
        actor: '',
        time: '',
        age: '',
        isHide: false,
        my_erp_id: ''
    })
    const handleImage = (e) => {
        setPage(e.target.files[0])
    }
    const addPhoto = async (id) => {
        try {
            console.log(id)
            console.log("OK")
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

        } catch (error) {
            console.log(error)
        }
    }
    const update = () => {
        setQuest({
            name: '',
            slug: '',
            desc: '',
            price: '',
            hard: 1,
            horror: 1,
            legend: '',
            min: '',
            max: '',
            actor: '',
            time: '',
            age: '',
            isHide: false,
            my_erp_id: ''
        })
        questData()
    }
    const handleChange = (e) => {
        const {name, value} = e.target
        setQuest({...quest, [name]: value})
    }
    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const fetch = await API.post('/admin/panel/add', {
                name: quest.name,
                slug: quest.slug,
                description: quest.desc,
                price: quest.price,
                hardId: quest.hard,
                horrorId: quest.horror,
                legend: quest.legend,
                minPlayers: quest.min,
                maxPlayers: quest.max,
                countActors: 1,
                playTime: quest.time,
                ageLimit: quest.age,
                isHide: false,
                myErpId: quest.my_erp_id
            }, {
                headers: {
                    Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
                }
            })

            if (!fetch.data.error) {
                await addPhoto(fetch.data.payload)
                update()
            } else {
                alert("Невозможно создать квест: " + fetch.data.message)
            }
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <>
            <form className="form" onSubmit={handleSubmit}>
                <p>Название квеста</p>
                <input type="text" name='name' value={quest.name} onChange={handleChange}/>
                <p>Название в URL</p>
                <input type="text" name='slug' value={quest.slug} onChange={handleChange}/>
                <p>ID с my-erp</p>
                <input type="text" name="my_erp_id" value={quest.my_erp_id} onChange={handleChange}/>
                <p>Тип квеста</p>
                <input type="text" name='desc' value={quest.desc} onChange={handleChange}/>
                <p>Цена</p>
                <input type="text" name='price' value={quest.price} onChange={handleChange}/>
                <p>Сложность</p>
                <select name="hard" defaultValue={1} onChange={handleChange}>
                    <option value={1}>1</option>
                    <option value={2}>2</option>
                    <option value={3}>3</option>
                </select>
                <p>Страх</p>
                <select name="horror" defaultValue={1} onChange={handleChange}>
                    <option value={1}>1</option>
                    <option value={2}>2</option>
                    <option value={3}>3</option>
                </select>
                <p>Легенда</p>
                <textarea name='legend' value={quest.legend} onChange={handleChange}></textarea>
                <p>Минимум игроков</p>
                <input type="text" name='min' value={quest.min} onChange={handleChange}/>
                <p>Максимум игроков</p>
                <input type="text" name='max' value={quest.max} onChange={handleChange}/>
                <p>Время (в минутах)</p>
                <input type="text" name='time' value={quest.time} onChange={handleChange}/>
                <p>Возраст</p>
                <input type="text" name='age' value={quest.age} onChange={handleChange}/>
                <p>Фотография квеста</p>
                <input type="file" onChange={handleImage}/>
                <button type="submit">Создать квест</button>
            </form>
        </>
    )
}
export default AddQuest