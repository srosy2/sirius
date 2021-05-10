import React from "react";
import s from "./Unknown.module.css";
import Node from "./Fragments/Node";

class Unknown extends React.Component {
    constructor(props) {
        super(props);

        this.nodes = [
            <Node/>
        ];
    }

    prepareList = () => {
        let nodes = [];
        for (let i = 0; i < this.props.list.length; i++){
            nodes.push(
                <Node key={this.props.list[i].id} label={this.props.list[i].label} color={this.props.list[i].color}/>
            );
        }
        return nodes;
    }

    render() {
        return (
            <div className={s.container}>
                <span className={s.sign}>Необходимо выучить:</span>
                <div className={s.node_container}>
                    {this.prepareList()}
                </div>
            </div>
        );
    }
}

export default Unknown;