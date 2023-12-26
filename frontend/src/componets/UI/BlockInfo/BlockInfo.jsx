import Feature from "./Feature/Feature"
import "./style.scss"
const BlockInfo = ({quest}) => {
    return (
        <div className="infoBlock">
                        <Feature quest={quest}/>
                        <div className="addServic">
                            <p className="title">Доп.Услуги:</p>
                            <div className="servic">
                                <p>Второй актер - 600 рублей​</p>
                                <p>Дополнительный игрок - 500 рублей (будни), 600 рублей (выходные)</p>
                                <p>Видеоролик прохождения квеста - 1.000 рублей (5-10 минут самых интересных моментов)</p>
                            </div>
                        </div>
                    </div>
    )
}

export default BlockInfo