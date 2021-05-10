import React from 'react';
import Graph from 'react-graph-vis';
import s from "./Main.module.css";
import {v4} from "uuid";
import Unknown from "../Unknown/Unknown";
import Routes from "../Routes/Routes";
import loading from "../../Images/Spinner-1s-200px.gif";

Array.prototype.unique = function() {
    var a = this.concat();
    for(var i=0; i<a.length; ++i) {
        for(var j=i+1; j<a.length; ++j) {
            if(a[i].id === a[j].id)
                a.splice(j--, 1);
        }
    }

    return a;
};

function checkElement(element, list){
    for (let i = 0; i < list.length; i++){
        if (element.id == list[i].id){
            return true;
        }
    }
    return false
}

function compare( a, b ) {
    if ( a.color < b.color ){
        return -1;
    }
    if ( a.color > b.color ){
        return 1;
    }
    return 0;
}

class Main extends React.Component {
    constructor(props) {
        super(props);

        this.options = {
            physics: true,
            nodes: {
                shape: "dot",
                scaling: {
                    min: 10,
                    max: 30
                },
                color: {
                    border: "#000000"
                }
            },
            layout: {
                hierarchical: false
            },
            edges: {
                color: {inherit: true},
                width: 0.5,
                // smooth: {
                //     type: "continious",
                // }
            },
            height: "900px"
        };

        this.state = {
            data: null,
            type: "both",
            loading: false,
            ontology: true
        }

        this.handleUploadImage = this.handleUploadImage.bind(this);
    }

    handleUploadImage = (e) => {
        e.preventDefault();

        this.setState({
            data: null,
            loading: true
        })

        let URL = "http://127.0.0.1:5000/upload/current/1";

        if (this.state.ontology){
            URL = "http://127.0.0.1:5000/upload/current/0"
        }

        const data = new FormData();

        for (let i = 0; i < this.uploadInputCompetentions.files.length; i++){
            data.append('competentions', this.uploadInputCompetentions.files[i]);
            data.append('filename', this.uploadInputCompetentions.files[i].name);
        }

        for (let i = 0; i < this.uploadInputNeeds.files.length; i++){
            data.append('needs', this.uploadInputNeeds.files[i]);
            data.append('filename', this.uploadInputNeeds.files[i].name);
        }

        fetch(URL, {
            method: "POST",
            body: data
        }).then((response) => {
            response.json().then((body) => {
                console.log(body)
                this.setState({
                    data: body,
                    loading: false
                });
            });
        });
    }

    simpleGraph = (data) => {
        const graph = {
            nodes: data.nodes,
            edges: data.edges
        };
        const events = {
            select: function (event) {
                var {nodes, edges} = event;
            }
        };

        return (
            <Graph
                key={v4()}
                graph={graph}
                options={this.options}
                events={events}
                getNetwork={network => {}}
            />
        );
    }

    superGraph = (data) => {

        for (let i = 0; i < data.needs.nodes.length; i++){
            data.needs.nodes[i]["opacity"] = 0.2;
            data.needs.nodes[i]["borderWidth"] = 6;
        }

        let nodes = data.competentions.nodes.concat(data.needs.nodes).unique();
        let edges = data.competentions.edges.concat(data.needs.edges);

        const graph = {
            nodes: nodes,
            edges: edges
        };



        const events = {
            select: function (event) {
                var {nodes, edges} = event;
            }
        };

        return (
            <Graph
                key={v4()}
                graph={graph}
                options={this.options}
                events={events}
                getNetwork={network => {}}
            />
        );
    }

    prepareGraph = () => {
        this.prepareRoutes();
        switch (this.state.type) {
            case "competentions":
                return this.simpleGraph(this.state.data.competentions);
            case "needs":
                return this.simpleGraph(this.state.data.needs);
            case "both":
                return this.superGraph(this.state.data);
        }
    }

    prepareRoutes = () => {
        let superRoutes = this.state.data.routes;

        let unknownNodes = this.state.data.needs.nodes;

        let tmp1 = [];
        for (let i = 0; i < unknownNodes.length; i++){
            if (!checkElement(unknownNodes[i], this.state.data.competentions.nodes)){
                tmp1.push(unknownNodes[i]);
            }
        }

        let tmp2 = [].concat.apply([], superRoutes)
        let tmp3 = []

        for (let i = 0; i < tmp1.length; i++){
            if (!checkElement(tmp1[i], tmp2)){
                tmp3.push(tmp1[i]);
            }
        }

        return {
            nodes: tmp3.sort(compare),
            routes: superRoutes
        };
    }

    render() {
        return (
            <div className={s.container}>
                <div className={s.form_container}>
                    <form onSubmit={this.handleUploadImage}>
                        <div className={s.check}>
                            <input type="checkbox" id="happy" name="happy" value="yes" checked={this.state.ontology}
                            onClick={() => this.setState({ontology: !this.state.ontology})}/>
                            <label htmlFor="happy">ГПН</label>
                        </div>
                        <div className={s.check}>
                            <input type="checkbox" id="happy" name="happy" value="yes" checked={!this.state.ontology}
                                   onClick={() => this.setState({ontology: !this.state.ontology})}/>
                            <label htmlFor="happy">ТПУ</label>
                        </div>
                        <div>
                            <div>Файлы компетенций</div>
                            <input accept={".docx"} ref={ref => this.uploadInputCompetentions = ref} type={"file"} multiple={"multiple"}/>
                        </div>
                        <div>
                            <div>Файлы требований</div>
                            <input accept={".docx"} ref={ref => this.uploadInputNeeds = ref} type={"file"} multiple={"multiple"}/>
                        </div>
                        <div>
                            <button className={s.start_button}>Отправить</button>
                        </div>
                        {this.state.loading ? (
                            <img className={s.loading} src={loading}/>
                        ) : ""}
                    </form>
                </div>
                {this.state.data !== null ? (
                    <div className={s.data}>
                        <div className={s.button_bar}>
                            <hr/>
                            <div className={s.subbutton_bar}>
                                <button onClick={() => this.setState({type: "competentions"})}>Граф Компетенций</button>
                                <button onClick={() => this.setState({type: "needs"})}>Граф Требований</button>
                                <button onClick={() => this.setState({type: "both"})}>Совмещённый Граф</button>
                            </div>
                            <hr/>
                        </div>
                        <div className={s.graph_container}>
                            {this.prepareGraph(this.state.data)}
                        </div>
                        <hr/>
                        {this.prepareRoutes().routes.length > -1 ?
                            <>
                                <Routes routes={this.prepareRoutes().routes}/>
                                <hr/>
                            </>
                        : ""}
                        <Unknown list={this.prepareRoutes().nodes}/>
                        <div className={s.space}></div>
                    </div>
                ) : ""}
            </div>
        );
    }

}

export default Main;