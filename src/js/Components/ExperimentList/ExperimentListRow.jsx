import React from 'react'
import { TableRow, TableRowColumn } from "material-ui/Table"
import DropDownMenu from 'material-ui/DropDownMenu'
import FlatButton from 'material-ui/FlatButton'
import MenuItem from 'material-ui/MenuItem'
import emitter from '../../Actions/EventEmitterAction'
import Moment from 'moment'

export default class ExperimentListRow extends React.Component {
    constructor() {
        super()
        this.state = {
            user: {
                user_id: 12345,
                user_name: '木村拓哉'
            },
            settings: {
                BOOK_ERROR_MSG: '请选择你的实验时间, 再提交预约申请!',
                BOOK_SUCCESS_MSG: '预约成功, 请进入在线学习页面！',
                DropDownMenu_disabled: false
            },
            default_value: {
                name: '边界层实验',
                location: '教四 303',
                times: ['1521644070840', '1521644182665'],
                time_selected: 0,
                status: false,
                experiment_id: 1111
            }
        }

    }

    componentWillMount() {
        const { name, locaton, time_selected } = this.state.default_value
        const { default_value } = this.state
        this.setState({
            ...this.state,
            default_value: {
                ...default_value,
                experiment_id: this.props.experiment_id
            }
        })
    }

    componentWillUnmount() {
        emitter.removeAllListeners()
    }

    studyExperiment = () => {
        window.open(`/#/${this.state.user.user_id}/experiment/${this.state.default_value.experiment_id}`, '_blank')
    }

    bookExperiment = () => {
        const { name, location, time_selected, experiment_id } = this.state.default_value
        const { BOOK_ERROR_MSG, BOOK_SUCCESS_MSG } = this.state.settings
        let request = {}

        if (this.state.default_value.time_selected !== 0) {
            request = {
                type: 'CONFIRM',
                payload: {
                    name,
                    location,
                    time_selected,
                    experiment_id
                }
            }
            this.eventEmitter = emitter.addListener('CONFIRM_RECEIVED', () => {
                this.setState({
                    ...this.state,
                    default_value: {
                        ...this.state.default_value,
                        status: true
                    },
                    settings: {
                        ...this.state.settings,
                        DropDownMenu_disabled: true
                    }
                })
            })
        }
        else {
            request = {
                type: 'ERROR',
                message: BOOK_ERROR_MSG
            }
        }
        emitter.emit(request.type, request)
    }

    render() {
        const TableRowColumnStyle = {
            textAlign: "center",
            padding: '0'
        }
        
        const { settings, default_value } = this.state

        return(
            <TableRow>
                <TableRowColumn style={TableRowColumnStyle}>{default_value.name}</TableRowColumn>
                <TableRowColumn style={TableRowColumnStyle}>{default_value.location}</TableRowColumn>
                <TableRowColumn style={TableRowColumnStyle}>
                    <DropDownMenu
                        ref="TimeMenu"
                        value={default_value.time_selected}
                        disabled={settings.DropDownMenu_disabled}
                        onChange={(event, index, value) => {
                            this.setState(
                                {
                                    ...this.state,
                                    default_value: {
                                        ...default_value,
                                        time_selected: value
                                    }
                                }
                            )
                        }}
                        labelStyle= {{
                            fontSize: '13px'
                        }}
                        menuItemStyle= {{
                            fontSize: '13px'
                        }}
                    >
                        <MenuItem value={0} label="请选择实验时间" primaryText="请选择实验时间" disabled />
                        {default_value.times.map((value, index) => 
                            < MenuItem key={index} value={value} primaryText={Moment(Number(value)).format("ll h:mm a")}/>
                        )}
                    </DropDownMenu>
                </TableRowColumn>
                <TableRowColumn style={TableRowColumnStyle}>
                    {default_value.status ?
                        <FlatButton label="学习" primary={true} onClick={this.studyExperiment.bind(this)} /> :
                        <FlatButton label="预约" primary={true} onClick={this.bookExperiment.bind(this)} />}
                </TableRowColumn>
            </TableRow>
        )
    }
}