import React from "react";

export function Images(props) {
    const {width, height} = props;
    console.log("images here");
    return <img src={"./placeHolder.png"} width={width} height={height} />
};