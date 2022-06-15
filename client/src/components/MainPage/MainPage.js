import React, { useEffect, useRef, useState } from 'react'
import {Header} from "../Header/Header";
import {Footer} from "../Footer/Footer";
import style from "./MainPage.module.scss";
import {Content} from "../Content/Content";
import { Toaster } from 'react-hot-toast'

export const MainPage = () => {

    return (
        <div className={style.MainPage}>
            <Header />
            <Content />
          <Toaster />
        </div>
    );
};
