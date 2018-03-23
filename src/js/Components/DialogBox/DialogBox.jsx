import React from 'react'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import RaisedButton from 'material-ui/RaisedButton';
import emitter from '../../Actions/EventEmitterAction'

export default class DialogBox extends React.Component {
    constructor() {
        super()
        this.state = {
            open: false,
            message: '',
            payload: {},
            settings: {
                width: "600px",
                actions: ''
            }
        }
    }

    confirm_tpl = (payload) => {

        return (
            <div>
                <div style={{fontSize: "14px"}}>你预约的实验是</div>
                <div style={{ fontSize: "18px", padding: "10px 20px" }}><b>{payload.name}</b></div>
                <div style={{ fontSize: "14px" }}>你做实验的地点是</div>
                <div style={{ fontSize: "18px", padding: "10px 20px" }}><b>{payload.location}</b></div>
                <div style={{ fontSize: "14px" }}>实验时间是</div>
                <div style={{ fontSize: "18px", padding: "10px 20px" }}><b>{(new Date(Number(payload.time_selected))).toLocaleString()}</b></div>
            </div>
        )
    }

    action_generator = (type) => {
        const actions = {
            normal: (<FlatButton
                label="好的"
                primary={true}
                onClick={this.handleClose}
            />),
            confirm: [
                <FlatButton
                    label="取消"
                    labelStyle={{color: '#6a6a6a'}}
                    primary={true}
                    onClick={this.handleClose}
                />,
                <RaisedButton
                    label="确认"
                    labelStyle={{color: '#fff'}}
                    primary={true}
                    onClick={this.confirm}
                />
            ]
        }

        switch(type) {
            case 'CONFIRM': {
                return actions.confirm
                break;
            }
            default: {
                return actions.normal
            }
        }
    }

    confirm = () => {
        emitter.emit('CONFIRM_RECEIVED', this.state.payload)
        this.handleClose()
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
        this.eventEmitter = emitter.addListener('ERROR', (request) => {
            this.setState({
                ...this.state,
                open: true,
                message: request.message,
                settings: {
                    ...this.state.settings,
                    width: '600px',
                    actions: this.action_generator(request.type)
                }
            })
        });

        this.eventEmitter = emitter.addListener("CONFIRM", (request) => {
            this.setState({
                ...this.state,
                open: true,
                message: this.confirm_tpl(request.payload),
                payload: request.payload,
                settings: {
                    ...this.state.settings,
                    width: '400px',
                    actions: this.action_generator(request.type)
                }
            })

        });
    }

    componentWillUnmount() {
        emitter.removeListener(this.eventEmitter);
    }

    render() {
        

        return (
            <Dialog
                actions={this.state.settings.actions}
                modal={false}
                open={this.state.open}
                onRequestClose={this.handleClose}
                contentStyle={{width: this.state.settings.width}}
            >
                {this.state.message}
            </Dialog>
        )
    }
}