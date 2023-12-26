import Quest from "./Quest/Quest";
import {useCallback, useEffect, useState} from "react";
import Api from "../../../API/Api";
import "./style.scss"


const QuestList = () => {
    const [quests, setQuests] = useState([]);
    const [load, setLoad] = useState(true)

    const dataQuest = useCallback(async() => {
        try {
            const data =  await Api.get("/get_quests")
                setQuests(data.data.payload)
                setLoad(false)

        }
        catch (error) {
            console.log(error.message())
        }
    }, [])

    useEffect(  () =>  {
        dataQuest()
    }, [dataQuest])

    if(load) {
        return (
            <div>
            </div>
        )
    }

    return (
        <div className="list">
            {quests.map((quest) => (
                <Quest key={quest.id} quest={quest}/>
            ))}
        </div>
    );
}

export default QuestList;
