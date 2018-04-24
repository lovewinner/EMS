import React from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import Theme_user from '../../Theme/Theme_user'

import Nav from '../../Components/Nav/Nav'
import SearchField from '../../Components/SearchField/SearchField'

export default class AppComponent extends React.Component {
    constructor() {
        super()
        this.state = {}
    }

    render() {

        return (
            <MuiThemeProvider muiTheme={getMuiTheme(Theme_user)}>
                <div>
                    <SearchField />
                    <Nav />
                    {this.props.children}
                </div>
            </MuiThemeProvider>
        )
    }
}