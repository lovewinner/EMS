import React from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import Snackbar from 'material-ui/Snackbar'
import Theme_user from '../../Theme/Theme_user'

import Nav from '../../Components/Nav/Nav'
import ExperimentList from '../../Components/ExperimentList/ExperimentList'
import DialogBox from '../../Components/DialogBox/DialogBox'
import LearningPanel from '../../Components/LearningPanel/LearningPanel'
import emitter from '../../Actions/EventEmitterAction'

import '../../../css/vendor_css'

export default class Home extends React.Component {
    constructor() {
        super()
        this.state = {
            snackbar_open: false,
            snackbar_message: '',
        }
    }

    showSnackbar = () => {
        this.setState({
            ...this.state,
            snackbar_open: true,
            snackbar_message: '实验添加成功!'
        })
    }

    componentDidMount = () => {
        this.eventEmitter = emitter.addListener('CONFIRM_RECEIVED', this.showSnackbar.bind(this))
    }

    comcomponentWillUnmount() {
        emitter.removeListener(this.eventEmitter);
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
                <div>
                    <Snackbar
                        open={this.state.snackbar_open}
                        message={this.state.snackbar_message}
                        autoHideDuration={4000}
                        bodyStyle={{borderRadius: '2px', backgroundColor: 'rgba(0, 0, 0, 0.87)'}}
                    />
                </div>
            </div>
            </MuiThemeProvider>
        )
    }
}