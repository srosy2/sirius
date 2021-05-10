import React from "react";
import Main from "./Components/Main/Main";
import Header from "./Components/Header/Header";
import s from "./App.module.css";

class App extends React.Component{
    render() {
        return (
            <div className={s.container}>
                <Header />
                <Main />
            </div>
        );
    }
}

export default App;
