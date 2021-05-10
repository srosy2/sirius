import React from 'react';
import logo from '../../Images/news-20200116-1579174858-n369a0.png'
import s from "./Header.module.css";

class Header extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={s.container}>
                <div className={s.navbar}>
                    <div className={s.logo_card}>
                        <img className={s.logo} src={logo} />
                        {/*<h2 className={s.label}>Проект по онтологиям</h2>*/}
                    </div>
                    <div>
                        <h1>Проект по онтологиям</h1>
                        <span className={s.label}>Разработка системы оценки компетенций сотрудника по используемым терминам</span>
                    </div>
                </div>
                <hr/>
            </div>
        );
    }
}

export default Header;