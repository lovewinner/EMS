import React from 'react'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import emitter from '../../Actions/EventEmitterAction'

export default class DialogBox extends React.Component {
    constructor() {
        super()
        this.state = {
            open: false,
            message: ''
        }
    }

    dialog_callback = () => {
        this.handleOpen()
    }

    handleOpen = () => {
        this.setState({
            ...this.state,
            open: true 
        });
    };

    handleClose = () => {
        this.setState({
            ...this.state,
            open: false
        });
    };

    componentDidMount() {
        this.eventEmitter = emitter.addListener("ALERT", (message) => {
            this.setState({
                open: true,
                message
            })
        });
    }

    componentWillUnmount() {
        emitter.removeListener(this.eventEmitter);
    }

    render() {
        const actions = [
            <FlatButton
                label="好的"
                primary={true}
                onClick={this.handleClose}
            />
        ];

        return (
            <Dialog
                actions={actions}
                modal={false}
                open={this.state.open}
                onRequestClose={this.handleClose}
            >
                {this.state.message}
            </Dialog>
        )
    }
}