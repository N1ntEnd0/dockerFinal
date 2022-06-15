import React, { useCallback, useEffect, useRef, useState } from 'react'
import style from "./Content.module.scss";
import {useFileSearch} from "../../requests/useFileSearch";
import {File} from "./File/File";
import {Footer} from "../Footer/Footer";
import { login } from '../../service/login'
import { useSelector } from 'react-redux'
import { toast } from 'react-hot-toast'

export const Content = () => {
    const [pageNumber, setPageNumber] = useState(1);
    const [selected, setSelected] = useState(false);
    const [selectedFiles, setSelectedFiles] = useState([])
    const authStatus = useSelector(state => state.authStatus.authStatus);

    const {
        files,
        hasMore,
        loading,
        error
    } = useFileSearch(authStatus, pageNumber);


    const observer = useRef();
    const lastFileElementRef = useCallback(node => {
        if (loading) return
        if (observer.current) observer.current.disconnect()
        observer.current = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting && hasMore) {
                setPageNumber(prevPageNumber => prevPageNumber + 1);
            }
        })
        if (node) observer.current.observe(node);
    }, [loading, hasMore]);

    const handleSelect = (file, checkSelected) => {
        if (selectedFiles === file) {
            setSelectedFiles([]);
            setSelected(false);
            checkSelected(false);
        }
        if (selectedFiles !== file && !selected) {
            setSelectedFiles(file);
            setSelected(true);
            checkSelected(true);
        }
        if (selectedFiles !== file && selected) {
            toast.error("Выбрать можно только 1 файл", {
                  position: 'top-right'
            });
        }
        /*if (selectedFiles.indexOf(file) === -1) {
            setSelectedFiles([...selectedFiles, file]);
            setSelected(true);
        } else {
            const copyArr = [...selectedFiles];
            copyArr.splice(selectedFiles.indexOf(file), 1)
            setSelectedFiles(copyArr);
            setSelected(copyArr.length > 0);
        }*/
    }
    return (
        <div className={style.Content}>
            <div className={style.Container}>
                {files.map((file, index) => {
                    if (files.length === index + 1) {
                        return (
                            <File
                                onClick={(file, checkSelected) => handleSelect(file, checkSelected)}
                                // onClick={(file) => handleSelect(file)
                                file={file}
                                ref={lastFileElementRef}
                            />
                        )
                    } else {
                        return <File file={file} onClick={(file, checkSelected) => handleSelect(file, checkSelected)} />
                    }
                })}
            </div>
            <div className={style.Info}>
                {
                    authStatus
                      ?
                      <div>
                          <div className={style.Info__loading} >{loading && 'Loading...'}</div>
                          <div className={style.Info__error} >{error && 'Error...'}</div>
                      </div>
                      :
                      <div className={style.Info__auth} >Авторизуйтесь для просмотра файлов</div>
                }
            </div>
            {selected && <Footer items={selectedFiles} />}
        </div>

    );
}