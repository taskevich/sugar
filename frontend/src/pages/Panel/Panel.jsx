import {Link} from "react-router-dom";
import {useCallback, useEffect, useState} from "react";
import API from "../../API/Api";
import AddQuest from "../../componets/admin/AddQuest";
import QuestAdmin from "../../componets/admin/QuestAdmin";
import Cookie from "js-cookie";
import {useNavigate} from "react-router";
import getAll from "../../API/getAll";
import "./style.scss"
import GalleryPage from "../../componets/admin/GalleryPage/GalleryPage";



const Panel = () => {
    const nav = useNavigate()
    const user = sessionStorage.getItem("auth")
    const [quests, setQuests] = useState([])

    const removeQuest = async (id) => {
        const data = await API.delete(`/admin/panel/remove/${id}`, {
            headers: {
                Authorization: `Bearer ${Cookie.get("access_token_cookie")}`,
            }
        })
        if (!data.data.error)
            await questData()
        else
            alert(data.data.message)
    }
    const questData = useCallback(async () => {
        try {
            const quest = await getAll("/admin/panel")
            setQuests(quest.payload.quests)
        } catch (error) {
            sessionStorage.setItem("auth", false)
            Cookie.set("access_token_cookie", "")
            nav("/admin")
            console.log(error)
        }

    }, [nav])
    useEffect(() => {
            questData()
        }, [questData]
    )

    return (
        <div className="admin">
            {user ? <>
                    <h1>Админ-Панель</h1>
                    <div className="element">
                        <div className="questList">
                            {
                                quests.map((quest) => (
                                    <div className="quest" key={quest.id}>
                                        <QuestAdmin quest={quest} removeQuest={removeQuest}/>
                                    </div>
                                ))
                            }
                        </div>
                        <AddQuest questData={questData}/>
                    </div>
                    <div className="galleryPage">
                        <GalleryPage/>
                    </div>
                </>
                :
                <>
                    <Link to="/admin">Заново</Link>
                </>}
        </div>
    );
};
export default Panel;
