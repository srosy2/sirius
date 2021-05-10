import React from "react";
import s from "./Node.module.css";

class Node extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={s.container} >
                <div className={s.line} style={{"backgroundColor": this.props.color}}></div>
                <div className={s.label}>{this.props.label}</div>
            </div>
        );
    }
}

export default Node;