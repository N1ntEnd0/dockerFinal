import './App.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import {presetGpnDefault, Theme} from "@consta/uikit/Theme";
import {MainPage} from "./components/MainPage/MainPage";
import { BrowserRouter } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Theme preset={presetGpnDefault}>
        <MainPage />
      </Theme>
    </BrowserRouter>
  );
}

export default App;
