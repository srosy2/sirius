import React from "react";
import s from "./Route.module.css";
import arrow from "../../../Images/down-arrow.png"

class Route extends React.Component{
    constructor(props) {
        super(props);
    }

    prepareList = () => {
        let list = [];
        for (let i = 0; i < this.props.list.length; i++){
            list.push(
                <div key={this.props.list[i].id} className={s.box}>
                    <img className={s.arrow} src={arrow} />
                    <span  className={s.el}>{`${i + 1}: ${this.props.list[i].label}`}</span>
                </div>
            );
        }
        return list;
    }

    render() {
        return (
            <div className={s.container} >
                <div className={s.line} style={{"backgroundColor": this.props.start.color}}></div>
                <div className={s.inner_container}>
                    <div className={s.known}><span className={s.start}>{this.props.start.label}</span></div>
                    <div className={s.wrapper}>{this.prepareList()}</div>
                </div>
            </div>
        );
    }
}

export default Route;