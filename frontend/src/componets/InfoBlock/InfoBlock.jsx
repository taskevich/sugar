import BlockInfo from "../UI/BlockInfo/BlockInfo"
import InfoImage from "../UI/InfoImage/InfoImage"
import "./style.scss"

const InfoBLock = ({quest}) => {
    return (
        <div className="info">
            <InfoImage quest={quest}/>
            <BlockInfo quest={quest}/>
        </div>
    )
}

export default InfoBLock