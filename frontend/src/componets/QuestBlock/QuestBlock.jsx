import QuestList from "../UI/QuestList/QuestList"
import "./style.scss"
const QuestBlock = () => {
    return (
        <div className="questBlock">
            <div className="wrapper">
                <h1>Наши квесты</h1>
                <QuestList/>
            </div>
        </div>
    )
}
export default QuestBlock;