import YMap from "./YMap";
import "./style.scss"
const Map = () => {
    return (
        <div className="map">
            <div className="wrapper">
                <div className="textBlock">
                    <h1>Наш адрес:</h1>
                    <p>ул . Сони Кривой, 69</p>
                </div>
                <div className="mapBlock">
                    <YMap></YMap>
                </div>
            </div>
        </div>
    )
}
export default Map;