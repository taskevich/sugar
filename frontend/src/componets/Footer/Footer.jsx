import {Link} from "react-router-dom";
import "./style.scss"

const Footer = () => {
    return (
        <footer>
            <Link to="/policy">Пользовательское соглашение</Link>
            <a href="https://chelyabinsk.mir-kvestov.ru/quests/saharnaya-vata-zverinets" target="_blank">
                <img src="https://chelyabinsk.mir-kvestov.ru/widgets/8085/img" width="210" alt="Отзывы на Квест в реальности Зверинец (Сахарная вата)" title="Отзывы на Квест в реальности Зверинец (Сахарная вата)"/>
            </a>
        </footer>
    )
}

export default Footer