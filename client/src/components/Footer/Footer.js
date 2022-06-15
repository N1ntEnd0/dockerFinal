import React from 'react';
import style from './Footer.module.scss';
import {Button} from "@consta/uikit/Button";
import { toast } from 'react-hot-toast'
import axios from 'axios'
import { useSelector } from 'react-redux'
import {API_URL} from "../../http";

export const Footer = ({ items }) => {
    const access = useSelector(state => state.accessToken.accessToken)

    const getLabel = () => {
        if (items) {
            if (items.length === 1) {
                return items[0].name;
            } else {
                return `Выбрано ${items.length} ${items.length < 5 ? 'элемента' : 'элементов'}`
            }
        } else {
            return 'Ничего не выбрано';
        }
    }

    const handleClick = () => {
        axios({
            method: 'POST',
            // url: `http://localhost:8000/api/v1/files/${items.id}/download/`,
            url: `${API_URL}/api/v1/files/${items.id}/download/`,
            headers: {
                'Authorization': `Bearer ${access}`
            },
        })
          .then(resp => {
            const element = document.createElement('a');
            element.href = resp.data.download_url;
            element.setAttribute('download', '123');
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
              // console.log('aa')



             /* const url = window.URL
                .createObjectURL(new Blob([resp.data.download_url]));
              const link = document.createElement('a');
              link.href = url;
              link.setAttribute('download', '123');
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);*/

            })
          // .then(resp => {
          //     axios({
          //         method: "GET",
          //         url: resp.data.download_url,
          //         responseType: 'blob',
          //         withCredentials: true
          //     })
          //       .then(response => {
          //           const url = window.URL
          //                 .createObjectURL(new Blob([response.data]));
          //           const link = document.createElement('a');
          //           link.href = url;
          //           link.setAttribute('download');
          //           document.body.appendChild(link);
          //           link.click();
          //           document.body.removeChild(link);
          //       })
          // })

          // .then(resp => {
          //   const url = window.URL
          //     .createObjectURL(new Blob([resp.data]));
          //   const link = document.createElement('a');
          //   link.href = url;
          //   link.setAttribute('download', '123');
          //   document.body.appendChild(link);
          //   link.click();
          //   document.body.removeChild(link);
        // })

            // axios({
            //     method: "GET",
            //     url: resp.data.download_url,
            //     responseType: 'blob',
            //     withCredentials: true
            // })
            //   .then(response => {
            //       const url = window.URL
            //             .createObjectURL(new Blob([response.data]));
            //       const link = document.createElement('a');
            //       link.href = url;
            //       link.setAttribute('download');
            //       document.body.appendChild(link);
            //       link.click();
            //       document.body.removeChild(link);
            //   })
          // console.log(resp.data.download_url)
        // })

    }

    return (
        <div className={style.Footer}>
            <Button onClick={handleClick} label="Скачать" />
            {/*<span>{getLabel()}</span>*/}
            <span>{items.name}</span>
        </div>
    );
}
