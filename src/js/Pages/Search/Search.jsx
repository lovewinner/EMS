import React from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import Theme_user from '../../Theme/Theme_user'


import Nav from '../../Components/Nav/Nav'
import SearchField from '../../Components/SearchField/SearchField'
import ExperimentLsit from '../../Components/ExperimentList/ExperimentList'

export default class Search extends React.Component {
    constructor() {
        super()
        this.state  = {

        }
    }

    render() {

        return (
            <MuiThemeProvider muiTheme={getMuiTheme(Theme_user)}>
                <div>
                    <div style={{ marginTop: '150px' }}>
                        <ExperimentLsit class_name="搜索结果："/>
                    </div>
                </div>
            </MuiThemeProvider>
        )
    }
}