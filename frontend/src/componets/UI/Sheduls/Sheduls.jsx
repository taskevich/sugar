import React from 'react';
import "./style.scss"

const Sheduls = ({id}) => {
    if (id === null || id === "") {
        return (
            <div></div>
        )
    }

    const url = `https://api-mir-kvestov.ru/api/v3/quests/${id}?city_id=6`
    return (
        <div className="sheduls">
            <h1>Расписание</h1>
            <iframe title="sheduls" className="shed" src={url} scrolling="yes" allowFullScreen="yes"
                    frameBorder="no"></iframe>
        </div>
    )
};

export default Sheduls;