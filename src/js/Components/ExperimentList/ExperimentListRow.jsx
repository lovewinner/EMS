import React from 'react'
import { TableRow, TableRowColumn } from "material-ui/Table"
import DropDownMenu from 'material-ui/DropDownMenu'
import FlatButton from 'material-ui/FlatButton'
import MenuItem from 'material-ui/MenuItem'
import emitter from '../../Actions/EventEmitterAction'

export default class ExperimentListRow extends React.Component {
    constructor() {
        super()
        this.state = {
            settings: {
                BOOK_ERROR_MSG: '请选择你的实验时间, 再提交预约申请!',
                BOOK_SUCCESS_MSG: '预约成功, 请进入在线学习页面！'
            },
            default_value: {
                name: '边界层实验',
                location: '教四 303',
                times: ['1521644070840', '1521644182665'],
                time_selected: 0,
                status: 0,
            }
        }

    }

    bookExperiment = () => {
        const { BOOK_ERROR_MSG, BOOK_SUCCESS_MSG } = this.state.settings
        let message = ''

        if (this.state.default_value.time_selected == 0) {
            message = BOOK_ERROR_MSG
        }
        else {
            message = BOOK_SUCCESS_MSG
        }

        emitter.emit("ALERT", message)
    }

    render() {
        const TableRowColumnStyle = {
            textAlign: "center",
            padding: '0'
        }

        const { default_value } = this.state

        return(
            <TableRow>
                <TableRowColumn style={TableRowColumnStyle}>{default_value.name}</TableRowColumn>
                <TableRowColumn style={TableRowColumnStyle}>{default_value.location}</TableRowColumn>
                <TableRowColumn style={TableRowColumnStyle}>
                    <DropDownMenu
                        ref="TimeMenu"
                        value={default_value.time_selected}
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
                            console.log(this.state)
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
                            < MenuItem key = { index }  value = { value } primaryText = {(new Date(Number(value))).toLocaleString()}/>
                        )}
                    </DropDownMenu>
                </TableRowColumn>
                <TableRowColumn style={TableRowColumnStyle}>
                    <FlatButton label="预约" primary={true} onClick={this.bookExperiment.bind(this)}/>
                </TableRowColumn>
            </TableRow>
        )
    }
}