import React from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import Theme_user from '../../Theme/Theme_user'

import Nav from '../../Components/Nav/Nav'
import ExperimentList from '../../Components/ExperimentList/ExperimentList'
import DialogBox from '../../Components/DialogBox/DialogBox'
import LearningPanel from '../../Components/LearningPanel/LearningPanel'

const muiTheme = getMuiTheme({
    appBar: {
        height: 48,
        color: "#2c5cd0",
    }
});

export default class Home extends React.Component {
    constructor() {
        super()
    }

    render() {
        return (
            <MuiThemeProvider muiTheme={getMuiTheme(Theme_user)}>
            <div>
                <div>
                    <Nav />
                    <ExperimentList class_name="流体力学"/>
                    <ExperimentList class_name="泵与风机" />
                    <DialogBox />
                </div>
                <div>
                    <LearningPanel />
                </div>
            </div>
            </MuiThemeProvider>
        )
    }
}