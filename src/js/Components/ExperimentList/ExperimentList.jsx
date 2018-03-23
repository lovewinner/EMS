import React from 'react'
import {
    Table,
    TableBody,
    TableHeader,
    TableHeaderColumn,
    TableRow
} from 'material-ui/Table';
import Card from 'material-ui/Card'
import FlatButton from 'material-ui/FlatButton'
import Dialog from 'material-ui/Dialog'



import ExperimentListRow from './ExperimentListRow'

export default class ExperimentList extends React.Component {
    constructor() {
        super()
        this.state = {
            table_settings: {
                fixedHeader: true,
                fixedFooter: true,
                stripedRows: false,
                showRowHover: false,
                selectable: false,
                multiSelectable: false,
                enableSelectAll: false,
                deselectOnClickaway: true,
                showCheckboxes: false,
            },
            default_value: {
                dialog_open: false,
                dialog_message: '',
                class_name: '流体力学',
                experiment_id: ['1022', '23231']
            }
        };
    }
    
    componentWillMount() {
        const { default_value } = this.state
        this.setState({
            ...this.state,
            default_value: {
                ...default_value,
                class_name: this.props.class_name
            }
        })
    }
    

    render() {
        const cardStyle = {
            width: "800px",
            margin: "5em auto",
        }
        const textAlignCenter = {
            textAlign: "center",
        }
        const listTitleStyle = {
            fontSize: "18px",
            color: "#565656",
            margin: '18px 0'
        }

        const actions = [
            <FlatButton
                label="好的"
                primary={true}
                onClick={this.handleClose}
            />
        ];

        const { table_settings, default_value } = this.state

        return (
            <div style={cardStyle}>
                <h5 style={listTitleStyle}>{default_value.class_name}</h5>
                <Card>
                    <Table 
                        selectable={table_settings.selectable}
                        bodyStyle={textAlignCenter}
                        headerStyle={textAlignCenter}
                        wrapperStyle={textAlignCenter}
                        
                    >
                        <TableHeader
                            displaySelectAll={table_settings.showCheckboxes}
                            adjustForCheckbox={table_settings.showCheckboxes}
                        >
                            <TableRow>
                                <TableHeaderColumn style={textAlignCenter}>实验名称</TableHeaderColumn>
                                <TableHeaderColumn style={textAlignCenter}>实验地点</TableHeaderColumn>
                                <TableHeaderColumn style={textAlignCenter}>实验时间</TableHeaderColumn>
                                <TableHeaderColumn style={textAlignCenter}>操作</TableHeaderColumn>
                            </TableRow>
                        </TableHeader>
                        <TableBody
                            displayRowCheckbox={table_settings.showCheckboxes}
                        >
                            {default_value.experiment_id.map((value, index) => 
                                <ExperimentListRow key={index} experiment_id={value}/>
                            )}
                            
                        </TableBody>
                    </Table>
                </Card>
                <Dialog
                    actions={actions}
                    modal={false}
                    open={this.state.default_value.dialog_open}
                    onRequestClose={this.handleClose}
                >
                    {this.state.default_value.dialog_message}
                </Dialog>
            </div>
        )
    }
}