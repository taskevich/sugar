import {Outlet} from "react-router-dom";
import Header from "../../componets/Header/Header";
import Footer from "../../componets/Footer/Footer";
import "./style.scss"
const Layout = () => {
    return (
        <>
            <Header/>
            <div className="container">
                    <Outlet/>
            </div>
            <Footer/>
        </>
    )
}
export default Layout;