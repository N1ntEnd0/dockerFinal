import React, { useEffect } from 'react'
import style from './Header.module.scss';
import {Button} from "@consta/uikit/Button";
import { useDispatch, useSelector } from 'react-redux'
import { setAccessAction } from '../../store/reducers/tokenStorage/accessStore'
import { GetRedirectUrl } from '../../requests/GetRedirectUrl'
import axios from 'axios'
import { useLocation } from 'react-router'
import { login } from '../../service/login'
import { setAuthStatusAction } from '../../store/reducers/authStorage/authStore'
import {API_URL} from "../../http";

export const Header = () => {
    const dispatch = useDispatch();

    const location = useLocation();

    useEffect(() => {
        let url = new URLSearchParams(location.search);
        if (url.has('state') && url.has('code')) {
            // console.log('state ' + url.get('state'));
            // console.log('code ' + url.get('code'))
            //
            // axios({
            //   method: 'POST',
            //   url: `http://share-my-gdrive.herokuapp.com/api/auth/social/o/google-oauth2/?state=${url.get('state')}&code=${url.get('code')}`,
            //   url: `http://localhost:8000/api/auth/social/o/google-oauth2/?state=${url.get('state')}&code=${url.get('code')}`,
              // headers: {
              //   'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
              // },
              // withCredentials: true,
            // })
            //   .then(res => {
            //   console.log('token ' + res.data.access)
            // })
            login(url.get('state'), url.get('code'))
              .then((resp) => {
                dispatch(setAuthStatusAction(true));
                return resp;
              })
              .then(response => {
                dispatch(setAccessAction(response.data.access));
                //todo save refresh
                // dispatch(setAccessAction(response.data.refresh));
                // localStorage.setItem('accessToken', response.data.access);
                // localStorage.setItem('refreshToken', response.data.refresh);
                // window.location.href='http://localhost:3000/';
                window.location.href=`${API_URL}/`;
              })
              .catch((err) => {
                //todo toast сервер временно недоступен
                console.log(err)
              })
        }
    }, [location.search])

    const handleClick = () => {
        GetRedirectUrl()
          .then(res => {
            window.location.href=res;
          });
    }

    return (
        <header className={style.Header}>
            <h1 className={style.Header__title}>
                Google Share
            </h1>
            <Button label="Войти" onClick={handleClick} />
        </header>
    );
}

