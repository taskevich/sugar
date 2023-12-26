import { YMaps, Map, Placemark } from '@pbe/react-yandex-maps';

const YMap = () => {
    const mapState ={
        center : [55.159900, 61.402544],
        zoom: 12
    }
    const markerPosition = [55.157228, 61.376763]
    return (
        <YMaps>
            <div style={{width: "100%", height: "100%"}}>
                <Map style={{maxWidth: "1000px",width: "100%", height:"100%"}} defaultState={mapState}>
                    <Placemark style={{background: "black"}} geometry={markerPosition}></Placemark>
                </Map>
            </div>
        </YMaps>
    )
}

export default YMap;