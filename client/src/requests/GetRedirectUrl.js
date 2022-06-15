import React, { useState } from 'react'
import axios from 'axios'
import {API_REDIRECT, API_URL} from "../http";

export const  GetRedirectUrl = () => {

  return axios({
    method: 'GET',
    // url:'https://share-my-gdrive.herokuapp.com/api/auth/social/o/google-oauth2',
    // url:'http://localhost:8000/api/auth/social/o/google-oauth2',
    url:`${API_URL}/api/auth/social/o/google-oauth2`,
    params: {
      // redirect_uri: 'http://localhost:3000/'
      // redirect_uri: `${API_URL}/`
      redirect_uri: `${API_REDIRECT}`
    },
    withCredentials: true,
  })
    .then(resp => {
      return resp.data.authorization_url;
    });
};

