import React from 'react';
import "./style.css"


const Brick = (props) => {
    return(
    <div className="brickContainer">
        <span>{props.heading}</span>
        <span>{props.name}</span>
    </div>
    )
}

export default Brick;