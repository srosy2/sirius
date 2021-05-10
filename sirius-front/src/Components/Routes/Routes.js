import React from "react";
import s from "./Routes.module.css";
import Route from "./Fragments/Route";

class Routes extends React.Component {
    constructor(props) {
        super(props);
    }

    prepareList = () => {
        let list = [];
        for (let i = 0; i < this.props.routes.length; i++){
            list.push(
                <Route
                    key={this.props.routes[i][0].id}
                    start={this.props.routes[i][0]}
                    list={this.props.routes[i].slice(1)}
                />
            );
        }
        return list;
    }

    render() {
        return (
            <div className={s.container}>
                <span className={s.sign}>Необходимо дополнить знания по данным путям:</span>
                <div className={s.routes_container}>
                    {this.prepareList()}
                </div>
            </div>
        );
    }
}

export default Routes;