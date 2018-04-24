import React from 'react'
import ReactDOM from 'react-dom'
import { hashHistory, Router, Route, IndexRoute, Link } from 'react-router'

import AppComponent from './Pages/AppComponent/AppComponent'
import Home from './Pages/Home/Home'
import Detail from './Pages/Detail/Detail'
import Search from './Pages/Search/Search'

const app = document.getElementById("app");

export default class App extends React.Component {
    constructor() {
        super()
    }

    render() {
        return (
            <div>{this.props.children}</div>
        )
    }
}


ReactDOM.render(
    <Router history={hashHistory}>
        <Route path='/' component={AppComponent}>
            <IndexRoute component={Home} />
            <Route path=':user_id/experiment/:experiment_id' component={Detail} />
            <Route path='search' component={Search} />
        </Route>
    </Router>
, app);
