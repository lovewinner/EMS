import React from 'react'
import { Card, CardActions, CardTitle, CardText } from 'material-ui/Card'
import FlatButton from 'material-ui/FlatButton'
import emitter from '../../Actions/EventEmitterAction'

export default class LearningPanel extends React.Component {
    constructor() {
        super()
        this.state = {
            user: {
                user_id: 12345,
                user_name: '木村拓哉'
            },
            reservations_list: [{
                    name: '边界层实验',
                    location: '教四 303',
                    time_selected: 1521644070840,
                    experiment_id: 123343
                },
                {
                    name: '空气流动实验',
                    location: '教四 303',
                    time_selected: 1521644182665,
                    experiment_id: 34234
                }
            ]
        }
    }

    timeFormat = (timeStamp) => {
        const time = new Date(Number(timeStamp))
        const localDateString = time.toLocaleDateString()
        let dayTime = ''
        if ( time.getHours() < 12) {
            dayTime = '早上 ' + time.getHours() + ' 点'
        }
        else {
            dayTime = time.getHours() - 12
            dayTime = '下午 ' + dayTime + ' 点'
        }
        return {
            localDateString,
            dayTime
        }
    }

    confirmReceivedResponse = (payload) => {
        const { reservations_list } = this.state
        this.setState({
            ...this.state,
            reservations_list: [
                ...reservations_list,
                payload
            ]
        })
    }

    componentDidMount = () => {
        this.eventEmitter = emitter.addListener('CONFIRM_RECEIVED', this.confirmReceivedResponse.bind(this))
    }

    comcomponentWillUnmount() {
        emitter.removeListener(this.eventEmitter);
    }


    studyExperiment = (experiment_id, event) => {
        window.open(`/#/${this.state.user.user_id}/experiment/${experiment_id}`, '_blank')
    }
    

    render() {

        const { reservations_list } = this.state

        const mainTitleStyle = {
            fontSize: '16px',
            color: '#565656',
            margin: '18px 60px',
            textAlign: 'right'
        }

        const cardStyle = {
            width: '200px',
            height: '200px',
            margin: '5px 10px',
        }


        if (this.state.reservations_list.length == 0) {
            return (<div></div>)
        }
        
        
        return (
            <div style={{display: 'flex', flexDirection: 'column', marginBottom: '50px'}}>
                <div style={mainTitleStyle}>已预约实验列表</div>
                <div style={{ marginRight: '50px', display: 'flex', flexDirection: 'row-reverse'}}>
                    {reservations_list.map((value, index) => {
                        const time = this.timeFormat(value.time_selected)
                        return (<Card key={index} style={cardStyle}>
                                    <CardText class="learning_card">
                                        <div>{value.name}</div>
                                        <div>{value.location}</div>
                                        <div>{time.localDateString}</div>
                                        <div>{time.dayTime}</div>
                                    </CardText>
                                    <CardActions style={{ display: 'flex', flexDirection: 'row-reverse'}}>
                                        <FlatButton label="学习" primary={true} value={value.experiment_id} onClick={this.studyExperiment.bind(this, value.experiment_id)} labelStyle={{color: "#3a75d7", verticalAlign: 'none'}}/>
                                    </CardActions>
                                </Card>)
                    })}
                </div>
                
            </div>
        )
    }
}