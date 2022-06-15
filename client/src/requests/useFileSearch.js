import React, {useEffect, useState} from 'react';
import axios from "axios";
import { useSelector } from 'react-redux'
import {API_URL} from "../http";

export const useFileSearch = (authorized, pageNumber) => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [files, setFiles] = useState([]);
    const [hasMore, setHasMore] = useState(false);
    const access = useSelector(state => state.accessToken.accessToken)

    useEffect(() => {
        if (authorized) {
            setLoading(true);
            setError(false);
            let controller = new AbortController();
            axios({
                method: 'GET',
                // url: 'http://localhost:8000/api/v1/files/',
                url: `${API_URL}/api/v1/files/`,
                params: { page: pageNumber, page_size: 10 },
                signal: controller.signal,
                headers: {
                    'Authorization': `Bearer ${access}`
                },
            }).then(res => {
                // console.log(res.data)
                setFiles(files => {
                    return [...files, ...res.data.results];
                });
                setHasMore(res.data.next !== null);
                setLoading(false);
            }).catch(err => {
                if (axios.isCancel(err)) return
                setError(true);
            })

            return () => controller.abort();
        }
    }, [pageNumber])

    return { loading, error, files, hasMore };
};

