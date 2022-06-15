import React, {useState, useRef} from 'react';
import style from './File.module.scss';
import {Tooltip} from "@consta/uikit/Tooltip";
import { IconCheck } from "@consta/uikit/IconCheck";
import { IconClose } from "@consta/uikit/IconClose";
import classNames from "classnames";
import axios from 'axios'

export const File = React.forwardRef(({file, onClick}, ref) => {
    const [selected, setSelected] = useState(false);
    const [hovered, setHovered] = useState(false);
    const [showTooltip, setShowTooltip] = useState(false);

    const anchorRef = useRef(null);

    const handleClick = (file) => {
         // setSelected(!selected)
         onClick(file, setSelected);
    }

    // const downloadImg = (url) => {
    //     return axios.get({
    //         method: 'GET',
    //         url: url,
    //         withCredentials: true,
    //     })
    //       .then(resp => {
    //           return resp.data
    //       })
    // }

    return (
        <div
            className={classNames(style.File, {
                [style.File_selected]: selected
            })}
            onMouseOver={() => setHovered(true)}
            onMouseOut={() => setHovered(false)}
            key={file.id}
            onClick={() => handleClick(file)}
            ref={ref}
        >
            {selected && (
                <div className={style.File__icon}>
                    {hovered
                        ? <IconClose size="s"/>
                        : <IconCheck size="s"/>}
                </div>
            )}
            <img
                src="https://findicons.com/files/icons/2813/flat_jewels/512/file.png"
                // src={file.iconLink}
                // src={() => downloadImg(file.thumbnailLink)}
                height="100"
                width="100"
            />
            <div
                className={style.File__name}
                ref={anchorRef}
                onMouseOver={() => setShowTooltip(true)}
                onMouseOut={() => setShowTooltip(false)}
            >
                {file.name}
            </div>
            {showTooltip && (
                <Tooltip
                    className={style.File__tip}
                    direction={"downCenter"}
                    size="s"
                    anchorRef={anchorRef}
                >
                    {file.name}
                </Tooltip>
            )}
        </div>
    );
});
