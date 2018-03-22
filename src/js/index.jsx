import React from 'react'
import ReactDOM from 'react-dom'
import { hashHistory, Router, Route, IndexRoute, Link } from 'react-router'

import Home from './Pages/Home/Home'
import Detail from './Pages/Detail/Detail'

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
        <Route path='/' component={App}>
            <IndexRoute component={Home} />
            <Route path='detail' component={Detail} />
        </Route>
    </Router>
, app);
