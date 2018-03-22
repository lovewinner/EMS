import React from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import { blue500 } from 'material-ui/styles/colors'

import Nav from '../../Components/Nav/Nav'
import ExperimentList from '../../Components/ExperimentList/ExperimentList'
import DialogBox from '../../Components/DialogBox/DialogBox'

const muiTheme = getMuiTheme({
    appBar: {
        height: 48,
        color: "#386cef",
    }
});

export default class Home extends React.Component {
    constructor() {
        super()
    }

    render() {
        return (
            <MuiThemeProvider muiTheme={muiTheme}>
                <div>
                    <Nav />
                    <ExperimentList class_name="流体力学"/>
                    <ExperimentList class_name="泵与风机" />
                    <DialogBox />
                </div>
            </MuiThemeProvider>
        )
    }
}