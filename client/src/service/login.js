import React from 'react'
import $api, {API_URL} from '../http'
import { useDispatch, useSelector } from 'react-redux'
import { setAccessAction } from '../store/reducers/tokenStorage/accessStore'
import axios from 'axios'

export const login = async (state, code) => {
    // const dispatch = useDispatch();

    try {
        return axios({
            method: 'POST',
            // url: `http://share-my-gdrive.herokuapp.com/api/auth/social/o/google-oauth2/?state=${url.get('state')}&code=${url.get('code')}`,
            // url: `http://localhost:8000/api/auth/social/o/google-oauth2/?state=${state}&code=${code}`,
            url: `${API_URL}/api/auth/social/o/google-oauth2/?state=${state}&code=${code}`,
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            withCredentials: true,
        })

    } catch (e) {
        console.log(e.response?.data?.details);
    }
}


