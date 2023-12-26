import React from 'react';
import { Link } from 'react-router-dom';
import deff from "../../../../assets/DefaultImage.png";
import "./style.scss"

const Quest = ({ quest }) => {
    return (
        <Link to={`/quest/${quest.slug}`} className="quest">

            {quest.files === null ? <img src={deff} alt="" />: <img src={`http://45.12.238.117:8000/get_image?image_path=/app/${Object.values(quest.files)[0]}`} alt=""/> }
            <div className="textBlock">
                <div className="textMain">
                    
                    <h1>{quest.name}</h1>
                    <p>{quest.description}</p>
                </div>
                <div className="limitText">
                    <p>+{quest.age_limit}</p>
                </div>
            </div>
            <button>Забронировать</button>
        </Link>
    )
}

export default Quest;