import { Route, Routes } from "react-router-dom";
import Layout from './pages/layout/Layout'
import Home from "./pages/Home/Home";
import QuestPage from "./pages/QuestPage/QuestPage";
import Login from "./pages/Login/Login";
import Panel from "./pages/Panel/Panel";
import UpdateQuest from "./componets/admin/Update";
import Privice from "./pages/Privice/Privice";


const App = () => {
  return (
      <Routes>
        <Route path="/" element={<Layout/>}>
          <Route index element={<Home/>}></Route>
            <Route path="/policy" element={<Privice/>}></Route>
          <Route path="/quest/:slug" element={<QuestPage/>}/>
        </Route>
        <Route path="/admin" element={<Login/>}/>
        <Route path="/admin/panel" element={<Panel/>}/>
        <Route path="/admin/panel/update/:slug" element={<UpdateQuest/>}/>
      </Routes>
  );
}

export default App;
